from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from card_app.models import Cart, CartItem
from product_app.models import Product
from card_app.api.serializers import CartItemSerializer
from product_app.api.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, pk):
    user = request.user
    try:
        cart_item = CartItem.objects.get(pk=pk, user=user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(
        cart_item, data=request.data, partial=True)
    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        old_quantity = cart_item.quantity

        if product.quantity == 0 or quantity > product.quantity:
            return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        # if quantity > old_quantity:
        #     product.quantity -= (quantity - old_quantity)
        # elif quantity < old_quantity:
        #     product.quantity += (old_quantity - quantity)

        # product.save()

        cart_item.totalPrice = quantity * product.price
        cart_item.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user

    product_id = request.data.get('product')
    quantity = int(request.data.get('quantity'))

    product = get_object_or_404(Product, pk=product_id)

    if quantity > product.quantity:
        return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)

    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, user=user, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.totalPrice = cart_item.quantity * product.price
    cart_item.save()

    # product.quantity -= quantity
    # product.save()

    serializer = CartItemSerializer(cart_item)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    user = request.user
    try:
        cart_item = CartItem.objects.get(pk=pk, user=user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # product = cart_item.product
    # product.quantity += cart_item.quantity
    # product.save()

    cart_item.delete()

    return Response({'success': 'Cart item removed successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cart_items(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user).select_related('product')
    serializer = CartItemSerializer(cart_items, many=True)

    products = [cart_item.product for cart_item in cart_items]
    product_serializer = ProductSerializer(products, many=True)

    data = {
        'cart_items': serializer.data,
        'products': product_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)