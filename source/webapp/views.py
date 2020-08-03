from webapp.models import Product
from django.shortcuts import redirect, get_object_or_404, render, Http404
from webapp.forms import ProductForm, SearchForm
from webapp.models import CATEGORY_CHOICES


def index_view(request):
    dropdown = []
    for i in CATEGORY_CHOICES:
        dropdown.append(i)
    form = SearchForm(data=request.GET)
    products = Product.objects.all().order_by('category', 'name')
    if form.is_valid():
        search = form.cleaned_data['search']
        if search:
            products = products.filter(name__icontains=form.cleaned_data['search'])
    return render(request, 'index.html', {'products': products, 'form': form, 'dropdown': dropdown})


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


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})


def add_view(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'add.html', {'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(**form.cleaned_data)
            return redirect('product', pk=product.pk)
        else:
            return render(request, 'add.html', {'form': form})


def update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = ProductForm(data={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'amount': product.amount,
            'price': product.price
        })
        return render(request, 'update.html', context={'form': form, 'product': product})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.amount = form.cleaned_data['amount']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect(product_view, pk=product.pk)
        else:
            return render(request, 'update.html', context={'form': form, 'product': product})


def delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect(index_view)
    return render(request, "delete.html", {'product': product})