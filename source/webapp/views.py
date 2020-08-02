from webapp.models import Product
from django.shortcuts import redirect, get_object_or_404, render
from webapp.forms import ProductForm


def index_view(request):
    products = Product.objects.all().order_by('category', 'name')
    return render(request, 'index.html', {'products': products})


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