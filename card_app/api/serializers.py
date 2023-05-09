from rest_framework import serializers
from card_app.models import Cart
from product_app.models import Product
from product_app.api.serializers import ProductSerializer
from user_app.models import User

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'quantity', 'total_price')

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError('Quantity should be greater than 0')
        if not User.objects.filter(id=data['user'].id).exists():
            raise serializers.ValidationError('User not found')
        product_data = data['product']
        product = Product.objects.filter(id=product_data['id']).first()
        if not product:
            raise serializers.ValidationError('Product not found')
        elif product.quantity < data['quantity']:
            raise serializers.ValidationError('Not enough products available')
        return data

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = Product.objects.get(id=product_data['id'])
        cart = Cart.objects.create(product=product, **validated_data)
        cart.total_price = cart.quantity * product.price
        cart.save()
        return cart

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product')
        instance.product = Product.objects.get(id=product_data['id'])
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_price = instance.quantity * instance.product.price
        instance.save()
        return instance