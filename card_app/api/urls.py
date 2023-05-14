from django.urls import path
from card_app.api import views

urlpatterns= [ 
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/items/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/items/<int:pk>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/items/', views.list_cart_items, name='list_cart_items'),
];   