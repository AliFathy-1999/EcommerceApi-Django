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
        fields = ["id","user","totalAmount","orderDate","status","address","note","payment_method","phone"]
    
    def __str__(self):
         return f"{self.user.username}'s order is ordered at {self.orderDate} and order status is {self.status}"    
   

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id","price","quantity","order_id","product"] 

