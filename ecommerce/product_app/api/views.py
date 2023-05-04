from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from product_app.models import Category
from product_app.api.serializers import CategorySerializer

@api_view()
def get_categories(request):
    Categories = Category.objects.all()
    serializer = CategorySerializer(Categories,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view()
def category_details(request,pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data,status=status.HTTP_200_OK)

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
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category,data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT);
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['DELETE'])
def deleted_category(request,pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({"message":"Category Deleted Successfully"},status=status.HTTP_204_NO_CONTENT);
