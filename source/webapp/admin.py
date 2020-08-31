from django.contrib import admin
from webapp.models import Product, Cart, Order, OrderProducts


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('pk', 'name', 'amount', 'price')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'phone', 'created_at',)
    ordering = ('-created_at',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProducts)