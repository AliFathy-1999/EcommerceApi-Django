from rest_framework import serializers
from wishlist_app.models import Wishlist
from django.contrib.auth import get_user_model
from product_app.models import Product

User = get_user_model()

class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product')