from urllib.parse import urlencode
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.models import Product
from django.shortcuts import redirect, get_object_or_404, render, Http404
from webapp.forms import ProductForm, SearchForm
from webapp.models import CATEGORY_CHOICES


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        context['dropdown'] = []
        for i in CATEGORY_CHOICES:
            context['dropdown'].append(i)
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
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

# def index_view(request):
#     dropdown = []
#     for i in CATEGORY_CHOICES:
#         dropdown.append(i)
#     form = SearchForm(data=request.GET)
#     products = Product.objects.all().order_by('category', 'name')
#     if form.is_valid():
#         search = form.cleaned_data['search']
#         if search:
#             products = products.filter(name__icontains=form.cleaned_data['search'])
#     return render(request, 'index.html', {'products': products, 'form': form, 'dropdown': dropdown})


def category_view(request, id):
    category = None
    for i in CATEGORY_CHOICES:
        if id in i:
            category = id
    if category:
        products = Product.objects.filter(category=category).order_by('name')
        print(category)
        return render(request, 'category.html', {'products': products})
    else:
        raise Http404


# def product_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'product.html', {'product': product})


class ProductView(DetailView):
    template_name = 'product.html'
    model = Product


# def add_view(request):
#     if request.method == 'GET':
#         form = ProductForm()
#         return render(request, 'product_create.html', {'form': form})
#     elif request.method == 'POST':
#         form = ProductForm(data=request.POST)
#         if form.is_valid():
#             product = Product.objects.create(**form.cleaned_data)
#             return redirect('product', pk=product.pk)
#         else:
#             return render(request, 'product_create.html', {'form': form})


class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


# def update_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         form = ProductForm(data={
#             'name': product.name,
#             'description': product.description,
#             'category': product.category,
#             'amount': product.amount,
#             'price': product.price
#         })
#         return render(request, 'product_update.html', context={'form': form, 'product': product})
#     elif request.method == 'POST':
#         form = ProductForm(data=request.POST)
#         if form.is_valid():
#             product.name = form.cleaned_data['name']
#             product.description = form.cleaned_data['description']
#             product.category = form.cleaned_data['category']
#             product.amount = form.cleaned_data['amount']
#             product.price = form.cleaned_data['price']
#             product.save()
#             return redirect(product_view, pk=product.pk)
#         else:
#             return render(request, 'product_update.html', context={'form': form, 'product': product})
#
#
class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


# def delete_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         product.delete()
#         return redirect(index_view)
#     return render(request, "product_delete.html", {'product': product})


class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')