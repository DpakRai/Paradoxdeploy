from rest_framework import routers
from django.urls import path
from django.urls.conf import include

from ecommerce.views import CartView, OrderView, ProductViewSet


router = routers.DefaultRouter()

router.register('product',ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('order/',OrderView.as_view(),name='order'),
    path('cart/',CartView.as_view(),name='cart'),
]