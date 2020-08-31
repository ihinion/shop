from django import forms
from webapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['username', 'address', 'phone']