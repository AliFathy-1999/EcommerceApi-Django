from django.urls import path
from .views import CartList, CartDetail

urlpatterns = [
    path('carts/', CartList.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
]