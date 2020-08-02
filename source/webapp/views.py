from webapp.models import Product
from django.shortcuts import redirect, get_object_or_404, render


def index_view(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})