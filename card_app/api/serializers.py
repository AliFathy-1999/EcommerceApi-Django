from rest_framework import serializers
from card_app.models import Cart
from product_app.models import Product
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from user_app.models import User

User = get_user_model()

class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'quantity', 'total_amount')
        read_only_fields = ('total_amount',)

    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError('Quantity should be greater than or equal to 0')
        if not User.objects.filter(id=data['user'].id).exists():
            raise serializers.ValidationError('User not found')
        product_data = data['product']
        product = Product.objects.filter(id=product_data.id).first()
        if not product:
            raise serializers.ValidationError('Product not found')
        if product.quantity < data['quantity']:
            raise serializers.ValidationError('Not enough products available')
        return data

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        user = validated_data['user']
        cart, created = Cart.objects.get_or_create(product=product, user=user)
        cart.quantity += quantity
        cart.save()
        return cart

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance