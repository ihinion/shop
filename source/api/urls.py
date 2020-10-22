from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet


app_name = 'api'

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    # path('get-token/', get_token_view, name='get_token'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    # path('articles/', ArticleListView.as_view(), name='article_list'),
    # path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete')
]