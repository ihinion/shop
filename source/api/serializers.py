from django.contrib.auth import get_user_model
from rest_framework import serializers
from webapp.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api:product-detail')

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'