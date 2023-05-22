from rest_framework import serializers
from wishlist_app.models import Wishlist
from django.contrib.auth import get_user_model
from product_app.models import Product
from product_app.api.serializers import ProductSerializer
User = get_user_model()

class WishlistSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product = ProductSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product')