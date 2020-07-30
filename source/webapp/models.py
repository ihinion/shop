from django.db import models


DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    ('other', 'Other'),
    ('food', 'Food'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('cars', 'Cars'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=2000, verbose_name='Description', null=True, blank=True)
    category = models.CharField(max_length=20, verbose_name='Category',
                                choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY)
    amount = models.IntegerField(verbose_name='Amount')
    price = models.DecimalField(verbose_name='Price', max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
