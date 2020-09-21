from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import View
from webapp.models import Product, Cart, Order, OrderProducts
from django.shortcuts import redirect, render
from webapp.forms import OrderForm


# class OrderCreateView(View):
#     def post(self, request, *args, **kwargs):
#         form = OrderForm(data=request.POST)
#         if form.is_valid():
#             order = Order.objects.create(
#                 username=form.cleaned_data['username'],
#                 address=form.cleaned_data['address'],
#                 phone=form.cleaned_data['phone']
#             )
#             for cart in Cart.objects.all():
#                 OrderProducts.objects.create(product=cart.product, amount=cart.amount, order=order)
#                 product = Product.objects.get(pk=cart.product.pk)
#                 product.amount = product.amount - cart.amount
#                 product.save()
#             Cart.objects.all().delete()
#             return redirect('index')
#         else:
#             carts = Cart.objects.all()
#             return render(request, 'cart/cart.html', context={'form': form, 'carts': carts})


class OrderCreateView_2(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        cart_products = Cart.objects.all()
        products = []
        order_products = []
        for item in cart_products:
            product = item.product
            amount = item.amount
            product.amount -= amount
            products.append(product)
            order_product = OrderProducts(order=order, product=product, amount=amount)
            order_products.append(order_product)
        OrderProducts.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ('amount',))
        cart_products.delete()
        if not self.request.user.is_anonymous:
            self.object.user = self.request.user
            self.object.save()
        return response

    def form_invalid(self, form):
        return redirect('cart_view')