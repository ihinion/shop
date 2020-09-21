from django.views.generic import ListView
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from webapp.models import Product, Cart
from django.shortcuts import redirect, get_object_or_404
from webapp.forms import OrderForm


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
    template_name = 'cart/cart.html'
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
