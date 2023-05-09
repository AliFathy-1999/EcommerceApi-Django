from rest_framework import generics
from card_app.models import Cart
from product_app.models import Product
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from product_app.api.serializers import ProductSerializer


class CartList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

# class CartList(generics.ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

# class CartDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
    
