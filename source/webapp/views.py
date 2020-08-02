from webapp.models import Product
from django.shortcuts import redirect, get_object_or_404, render


def index_view(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})
