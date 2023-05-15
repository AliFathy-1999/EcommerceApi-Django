from django.urls import path
from wishlist_app.api.views import WishlistListCreateView, WishlistDeleteView

urlpatterns = [
    path('', WishlistListCreateView.as_view(), name='wishlist-list-create'),
    path('<int:pk>/', WishlistDeleteView.as_view(), name='wishlist-delete'),
]