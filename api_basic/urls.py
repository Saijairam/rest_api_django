from django.urls import path,include
from .views import Article_detail_class,ArticleAPIView,GenericAPIView,ArticleViewSet,ArticleGViewSet,ArticleMViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('article',ArticleMViewSet,basename='article')

urlpatterns = [
    path('viewsets/',include(router.urls)),
    path('viewsets/<int:pk>/',include(router.urls)),
    # path('article/',views.article_list,name='article_list'),
    path('article/',ArticleAPIView.as_view(),name='article_list'),
    # path('article/<int:pk>',article_detail,name='article_detail'),
    path('article/<int:id>/',Article_detail_class.as_view(),name='article_detail'),

    path('generic/article/',GenericAPIView.as_view(),name='generic_api_view'),
    path('generic/article/<int:id>/',GenericAPIView.as_view(),name='generic_api_update')
]