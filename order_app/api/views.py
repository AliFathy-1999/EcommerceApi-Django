from order_app.models import Order,OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user_app.models import Address
from card_app.models import Cart
from card_app.api.serializers import CartSerializer
from django.shortcuts import get_object_or_404

class OrderList(APIView):
    """
    List all Orders, or create a new Order.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        try:
            cart = Cart.objects.get(user=request.user)
            address = Address.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            order_items = Cart.objects.filter(product_id=cart.product.id)
            total_price = 0
            for item in order_items:
                total_price += item.quantity * item.product.price
                
            order = Order(
                user_id=request.user.id,
                totalAmount=total_price,
                status='PENDING',
                address_id = address.id
            )
            order.save()
            for item in order_items:
                order_item = OrderItem(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                order_item.save()
                product = item.product
                product.quantity -= item.quantity
                product.save()
            
                cart.delete()
                serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception  as e:
            return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
        
    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order, data=request.data)
        if order.status == 'PENDING':
            order.status = 'CANCELLED'
            order.save()
            return Response({'message': 'Order Cancelled successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
        permission_classes = [IsAuthenticated]
        def get(self, request, *args, **kwargs):
            try:
                order_id = kwargs.get('order_id')
                order = get_object_or_404(Order, id=order_id, user=request.user)
                order_items = OrderItem.objects.filter(order_id = order.id)
                order_items_list = []
                item = {}
                for order_item in order_items:
                    item["id"] = order_item.id
                    item['price'] = order_item.price
                    item['quantity'] = order_item.quantity
                    item['order_id'] = order_item.order_id
                    item['product_id'] = order_item.product_id
                serializer = OrderSerializer(order)
                return Response({'order': serializer.data,"orderitems":order_items_list}, status=status.HTTP_200_OK)
            except Exception as e:
                 return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);