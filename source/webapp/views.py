from urllib.parse import urlencode

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from webapp.models import Product, Cart, Order, OrderProducts
from django.shortcuts import redirect, get_object_or_404, render, Http404
from webapp.forms import ProductForm, SearchForm, OrderForm
from webapp.models import CATEGORY_CHOICES


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5
    ordering = ['category', 'name']

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(amount__gt=0)
        if self.search_value:
            query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProductView(DetailView):
    template_name = 'product.html'
    model = Product


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm
    permission_required = 'webapp.product_add'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm
    permission_required = 'webapp.product_change'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')
    permission_required = 'webapp.product_delete'


class CartCreateView(View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        try:
            cart_ids = self.request.session.get('cart_ids', [])
            cart = Cart.objects.get(product=product, pk__in=cart_ids)
            if cart.amount < product.amount:
                cart.amount += 1
                cart.save()
        except ObjectDoesNotExist:
            if product.amount > 0:
                cart_product = Cart.objects.create(product=product, amount=1)
                cart_ids = self.request.session.get('cart_ids', [])
                if cart_product.id not in cart_ids:
                    cart_ids.append(cart_product.id)
                self.request.session['cart_ids'] = cart_ids
        return redirect('index')


class CartView(ListView):
    template_name = 'cart.html'
    model = Cart
    context_object_name = 'carts'
    form = OrderForm

    def get_queryset(self):
        cart_ids = self.request.session.get('cart_ids', [])
        return Cart.objects.filter(pk__in=cart_ids)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        total = 0
        cart_ids = self.request.session.get('cart_ids', [])
        for obj in Cart.objects.filter(pk__in=cart_ids):
            total += obj.amount * obj.product.price
        context['total'] = total
        context['form'] = self.form
        return context


class CartDeleteView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        cart_ids = self.request.session.get('cart_ids', [])
        cart = Cart.objects.get(product=product, pk__in=cart_ids)
        cart.delete()
        return redirect('cart_view')


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            order = Order.objects.create(
                username=form.cleaned_data['username'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone']
            )
            for cart in Cart.objects.all():
                OrderProducts.objects.create(product=cart.product, amount=cart.amount, order=order)
                product = Product.objects.get(pk=cart.product.pk)
                product.amount = product.amount - cart.amount
                product.save()
            Cart.objects.all().delete()
            return redirect('index')
        else:
            carts = Cart.objects.all()
            return render(request, 'cart.html', context={'form': form, 'carts': carts})