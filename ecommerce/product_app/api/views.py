from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from product_app.models import Category,Product
from product_app.api.serializers import CategorySerializer,ProductSerializer
from http import *
@api_view(['GET'])
def get_categories(request):
    try:
        Categories = Category.objects.all()
        serializer = CategorySerializer(Categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        raise Exception('Error in getting categories')
    
@api_view(['GET'])
def category_details(request,pk):
    try:
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"message":"Invalid Category Id"},status.HTTP_404_NOT_FOUND);

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(serializer.data,status=status.HTTP_201_CREATED);
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_category(request,pk):
    try:
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category,data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT);
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({"message":"Invalid Category Id"},status.HTTP_404_NOT_FOUND);
@api_view(['DELETE'])
def deleted_category(request,pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({"message":"Category Deleted Successfully"},status=status.HTTP_204_NO_CONTENT);
    except Category.DoesNotExist:
        return Response({"message":"Invalid Category Id"},status.HTTP_404_NOT_FOUND);
# Products APIS 

@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        raise Exception('Error in getting products')   
     
@api_view(['GET'])
def product_details(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"message":"Invalid product Id"},status.HTTP_404_NOT_FOUND);

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(serializer.data,status=status.HTTP_201_CREATED);
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_product(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product,data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT);
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"message":"Invalid product Id"},status.HTTP_404_NOT_FOUND);
@api_view(['DELETE'])
def deleted_product(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({"message":"Product Deleted Successfully"},status=status.HTTP_204_NO_CONTENT);
    except Product.DoesNotExist:
        return Response({"message":"Invalid product Id"},status.HTTP_404_NOT_FOUND);