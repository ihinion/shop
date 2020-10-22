from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, OrderViewSet, get_token_view


app_name = 'api'

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('', include(router.urls)),
]