from order_app.models import Order,OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user_app.models import Address
from card_app.models import Cart,CartItem
from card_app.api.serializers import CartSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAddressOwner
class OrderList(APIView):
    """
    List all Orders, or create a new Order.
    """
    permission_classes = [IsAuthenticated,IsAddressOwner]
    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            serializer = CartSerializer(cart)
            cart_items = CartItem.objects.filter(cart=cart.id)
            if (cart_items.count() == 0):
                raise Exception('There is no Cart Item is added');
            
            total_price = 0
            for item in cart_items:
                total_price += item.quantity * item.product.price   
            user_address = int(request.POST.get('address'))
  
            order_data = {
                "user" : request.user.id,
                "totalAmount":total_price,
                "status":'PENDING',
                "address" : user_address,
                "note" : request.POST.get('note'),
                "payment_method" : request.POST.get('payment_method'),
                "phone" : request.POST.get('phone'),
            }
            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                order = serializer.save()
                for item in cart_items:
                    order_item = OrderItem(order=order,product=item.product,price=item.product.price,quantity=item.quantity)
                    order_item.save()
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()
                cart_items.delete()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception  as e:
                return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
        
    def put(self, request, order_id):
            order = get_object_or_404(Order, id=order_id, user=request.user)
            if order.status == 'PENDING':
                order.status = 'CANCELLED'
                order.save()
                return Response({'message': 'Order Cancelled successfully'}, status=status.HTTP_200_OK)
            return Response({'message':"Error, Order status must be Pending to cancel it" }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
        permission_classes = [IsAuthenticated,IsAddressOwner]
        def get(self, request, *args, **kwargs):
            try:
                order_id = kwargs.get('order_id')
                order = get_object_or_404(Order, id=order_id, user=request.user)
                serializer = OrderSerializer(order)
                order_items = OrderItem.objects.filter(order_id = order.id)
                order_items_serializer = OrderItemSerializer(order_items, many=True)
                return Response({'order': serializer.data,"orderitems":order_items_serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);

        def put(self, request, *args, **kwargs):
            try:
                order_id = kwargs.get('order_id')
                order = get_object_or_404(Order, id=order_id, user=request.user)
                serializer = OrderSerializer(order, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                if order.status == 'PENDING':
                    address = request.POST.get('address')
                    if address is not None:
                        order.address.id = int(address)
                    
                    phone = request.POST.get('phone')
                    if phone is not None:
                        order.phone = phone
                    
                    note = request.POST.get('note')
                    if note is not None:
                        order.note = note
                        
                    payment_method = request.POST.get('payment_method')
                    if payment_method is not None:
                        order.payment_method = payment_method                        
                    serializer.save()
                    return Response(serializer.data)
            except Exception as e:
                return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
