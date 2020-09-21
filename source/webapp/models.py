from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


CATEGORY_CHOICES = (
    ('other', 'Other'),
    ('food', 'Food'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('cars', 'Cars'),
)
DEFAULT_CATEGORY = CATEGORY_CHOICES[0][0]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=2000, verbose_name='Description', null=True, blank=True)
    category = models.CharField(max_length=20, verbose_name='Category',
                                choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY)
    amount = models.IntegerField(verbose_name='Amount', validators=[MinValueValidator(0)])
    price = models.DecimalField(verbose_name='Price', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Cart(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.PROTECT, verbose_name='Cart')
    amount = models.IntegerField(verbose_name='Amount', validators=[MinValueValidator(0)])

    def __str__(self):
        return f'Product: {self.product.name}, amount: {self.amount}'


class Order(models.Model):
    username = models.CharField(max_length=40, verbose_name='Username')
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    address = models.CharField(max_length=50, verbose_name='Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL, \
                             related_name='orders', verbose_name='User')

    def __str__(self):
        return f'Order #: {self.pk}, user: {self.username}'

    def get_total(self):
        total = 0
        for product in self.order_products.all():
            total += product.product.price * product.amount
        return total


class OrderProducts(models.Model):
    order = models.ForeignKey('webapp.Order', related_name='order_products', on_delete=models.CASCADE,
                              verbose_name='Order')
    product = models.ForeignKey('webapp.Product', related_name='product_orders', on_delete=models.CASCADE,
                                verbose_name='Product')
    amount = models.IntegerField(verbose_name='Amount')