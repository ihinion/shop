from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.permissions import GETModelPermissions
from api.serializers import ProductSerializer, OrderSerializer
from webapp.models import Product, Order


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class OrderViewSet(ViewSet):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [GETModelPermissions()]
        else:
            return [AllowAny()]

    def list(self, request):
        objects = Order.objects.all()
        slr = OrderSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = OrderSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            order = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        slr = OrderSerializer(order, context={'request': request})
        return Response(slr.data)