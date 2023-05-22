from django.shortcuts import get_object_or_404
from rest_framework import generics
from wishlist_app.models import Wishlist
from wishlist_app.api.serializers import WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from product_app.models import Product

class WishlistListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(user=self.request.user, product=product)
        
        
class WishlistDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
    
