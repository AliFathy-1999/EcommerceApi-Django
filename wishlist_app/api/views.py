from rest_framework import generics
from wishlist_app.models import Wishlist
from wishlist_app.api.serializers import WishlistSerializer
from rest_framework.permissions import IsAuthenticated

class WishlistListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
    
