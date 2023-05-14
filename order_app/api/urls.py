from django.urls import path,include
from .views import * 

urlpatterns = [
    path('',OrderList.as_view()),
    path('<int:order_id>',OrderList.as_view(),name='cancelled'),
    path('order/<int:order_id>',OrderDetail.as_view(),name='order_detail'),
]
