from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status,filters
from django.db.models import Count
from product_app.models import Category,Product
from product_app.api.serializers import CategorySerializer,ProductSerializer
from product_app.api.pagination import ProductPagination
from http import *
from django_filters.rest_framework import DjangoFilterBackend
# ***
# *** Categories APIS ***
# ***
@api_view(['GET'])
def get_categories(request):
    try:
        Categories = Category.objects.annotate(num_products=Count('product')).values('id', 'name', 'categoryPic', 'num_products')
        category_list = list(Categories) 
        paginator = ProductPagination()
        paginated_categories = paginator.paginate_queryset(category_list, request)
        Response.status_code = status.HTTP_200_OK;
        return paginator.get_paginated_response({"categories" : paginated_categories})
    except Category.DoesNotExist:
        raise Exception('Error in getting categories')
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
@api_view(['GET'])
def category_details(request,pk):
    try:
        category = Category.objects.get(pk=pk)
        categoryProducts = Product.objects.filter(categoryId = category.id).values("id", "name", "description", "quantity","productPic","price")
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(categoryProducts, request)
        serializer = CategorySerializer(category)
        Response.status_code = status.HTTP_200_OK;
        return paginator.get_paginated_response({"category":serializer.data,"products":paginated_products})
    except Category.DoesNotExist:
        return Response({"message":"Invalid Category Id"},status.HTTP_404_NOT_FOUND);
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);

@api_view(['POST'])
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data,status=status.HTTP_201_CREATED);
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
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
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
@api_view(['DELETE'])
def deleted_category(request,pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({"message":"Category Deleted Successfully"},status=status.HTTP_204_NO_CONTENT);
    except Category.DoesNotExist:
        return Response({"message":"Invalid Category Id"},status.HTTP_404_NOT_FOUND);
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
# ***
# *** Products APIS ***
# ***
@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()
        paginator = ProductPagination();
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page,many=True)
        Response.status_code = status.HTTP_200_OK;
        return paginator.get_paginated_response(serializer.data)
    except Category.DoesNotExist:
        raise Exception('Error in getting products')
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);  
     
@api_view(['GET'])
def product_details(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"message":"Invalid product Id"},status.HTTP_404_NOT_FOUND);
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);

@api_view(['POST'])
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data,status=status.HTTP_201_CREATED);
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
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
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
@api_view(['DELETE'])
def deleted_product(request,pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({"message":"Product Deleted Successfully"},status=status.HTTP_204_NO_CONTENT);
    except Product.DoesNotExist:
        return Response({"message":"Invalid product Id"},status.HTTP_404_NOT_FOUND);
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);
    
@api_view(['GET'])
def search_on_products(request):   
    try:
        key = request.query_params.get('key');
        searchProducts = Product.objects.all();      
        if key:
            searchProducts = searchProducts.filter(name__icontains=key)
        paginator = ProductPagination();
        result_page = paginator.paginate_queryset(searchProducts, request)
        serializer = ProductSerializer(result_page,many=True)
        Response.status_code = status.HTTP_200_OK;
        return paginator.get_paginated_response(serializer.data)
    except Category.DoesNotExist:
        raise Exception('Error in getting products')
    except Exception  as e:
        return Response({"message":e.args[0]},status.HTTP_400_BAD_REQUEST);    