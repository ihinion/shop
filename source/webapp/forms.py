from django import forms
from django.forms import widgets
from webapp.models import CATEGORY_CHOICES
from django.core.validators import MinValueValidator


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name', required=True)
    description = forms.CharField(max_length=2000, label='Description', required=False, widget=widgets.Textarea)
    category = forms.ChoiceField(required=True, label='Category', choices=CATEGORY_CHOICES,
                                 initial=CATEGORY_CHOICES[0][0])
    amount = forms.IntegerField(label='Amount', min_value=0, required=True)
    price = forms.DecimalField(label='Price', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)],
                               required=True)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label=None)