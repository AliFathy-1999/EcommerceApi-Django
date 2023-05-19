from django.urls import path,include
from .views import * 

urlpatterns = [
    path('',OrderAPI.as_view()),
    path('<int:order_id>',OrderAPI.as_view(),name='cancelled'),
    path('order/<int:order_id>',OrderDetail.as_view(),name='order_detail'),
    path('payment/',CheckOutView.as_view(),name='create-checkout-session'),
]
