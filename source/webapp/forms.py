from django import forms
from django.forms import widgets
from webapp.models import CATEGORY_CHOICES, Product
from django.core.validators import MinValueValidator


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')