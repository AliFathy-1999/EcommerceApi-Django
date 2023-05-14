from rest_framework import serializers
from order_app.models import Order,OrderItem
import re
from django.contrib.auth import get_user_model
from user_app.models import Address
from product_app.api.serializers import ProductSerializer

User = get_user_model()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id","user","totalAmount","orderDate","status","address"]
    def __str__(self):
         return f"{self.user.username}'s order is ordered at {self.orderDate} and order status is {self.status}"    
    
    def validate_status(self, value):
        if value not in [choice[0] for choice in Order.ORDER_STATUS_CHOICES]:
            raise serializers.ValidationError('Invalid status value')
        return value 
    def validate_totalAmount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Invalid Total Amount value')
        return value 
    def validate(self, data):
        user = data.get('user')
        if not user:
            raise serializers.ValidationError('User field is required')

        address = data.get('address')
        if not address:
            raise serializers.ValidationError('Address field is required')
        return data    

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id","price","quantity","order_id","product_id"] 

