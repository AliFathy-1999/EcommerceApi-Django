from order_app.models import Order,OrderItem,PaymentToken
from .serializers import OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from card_app.models import Cart,CartItem
from card_app.api.serializers import CartSerializer
from django.shortcuts import get_object_or_404,redirect
from .permissions import IsAddressOwner
from django.db import transaction
import stripe
from stripe.error import AuthenticationError
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
import secrets
class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]
      
    def post(self, request):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            cart_items = CartItem.objects.filter(cart=cart.id)
            if (cart_items.count() == 0):
                raise Exception('There is no Cart Item is added');
            
            total_price = 0
            for item in cart_items:
                total_price += item.quantity * item.product.price 
            line_items = []
            for item in cart_items:
                line_item = {
                    'price_data' :{
                        'currency' : 'usd',  
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100)
                    },
                    'quantity' : item.quantity
                }
                line_items.append(line_item)
            token = secrets.token_hex(16) # Generate token
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                    success_url = f'{settings.SITE_URL}/orderiscreated?token={token}&user={request.user.id}',
                    cancel_url = f'{settings.SITE_URL}/orderiscancelled',
            )
            payment_token = PaymentToken(user=request.user,token=token,is_valid=True)
            payment_token.save()   
            return Response({"checkouturl":checkout_session.url},status.HTTP_303_SEE_OTHER);
        except Exception as e:
            return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
        
class OrderAPI(APIView):
    """
    List all Orders, or create a new Order.
    """
    permission_classes = [IsAuthenticated,IsAddressOwner]
    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    @transaction.atomic
    def post(self, request, format=None):
        try:
            token = request.POST.get('token')
            if(token):
                payment_token = PaymentToken.objects.get(user_id=request.user.id,token=token,is_valid=True)
                if not payment_token :
                    raise AuthenticationError("UnAuthorized Access");
                payment_token.is_valid=False;
                payment_token.save()
            
            cart = get_object_or_404(Cart, user=request.user)
            serializer = CartSerializer(cart)
            
            cart_items = CartItem.objects.filter(cart=cart.id)
            if (cart_items.count() == 0):
                raise Exception('There is no Cart Item is added');
            
            total_price = 0
            for item in cart_items:
                total_price += item.quantity * item.product.price   

            order_data = {
                "user" : request.user.id,
                "totalAmount":total_price,
                "status":'PENDING',
                "address" : request.POST.get('address'),
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
        except AuthenticationError as e:
            return Response({"message":e.args[0]},status.HTTP_402_PAYMENT_REQUIRED);
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
            

