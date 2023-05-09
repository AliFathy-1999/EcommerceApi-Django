from django.urls import path
from .views import CartList, CartDetail

urlpatterns = [
    path('cart/', CartList.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
]