from rest_framework import serializers
from product_app.models import Category,Product
# ,Product
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import re
import os

def validate_picture(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png','.jfif','.jpg']
    if not ext.lower() in valid_extensions:
        raise serializers.ValidationError("File extension not supported. Supported extensions are .png, .jpeg, .jpg, .jfif.")
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise serializers.ValidationError("File size exceeds the limit of 5 MB.")
    else:
        return value;
def name_length(value):
    if len(value) < 3 :
        raise serializers.ValidationError("This Field must be at least 3 characters");
    if len(value) > 40 :
        raise serializers.ValidationError("This Field name must be not more than 40 characters");
    
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    categoryPic = serializers.ImageField()
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data);
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.categoryPic = validated_data.get('categoryPic',instance.categoryPic)
        instance.save();
        return instance;


    def validate_name(self,value):
        if  not re.search('[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("Field must contain only alphabetic characters");
        else:
            return value
        
    def validate_categoryPic(self,value):
        return validate_picture(value)
        
def description_length(value):
    if len(value) < 6 :
        raise serializers.ValidationError("This Field must be at least 6 characters");
    if len(value) > 255 :
        raise serializers.ValidationError("This Field name must be not more than 255 characters");
    
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField(validators=[description_length])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    productPic = serializers.ImageField()
    avgRating = serializers.DecimalField(max_digits=4, decimal_places=2)
    quantity = serializers.IntegerField()
    # categoryId = serializers.ForeignKey()
    def __str__(self):
        return self.name
    def create(self, validated_data):
        return Product.objects.create(**validated_data);
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name);
        instance.description = validated_data.get('description',instance.description);
        instance.productPic = validated_data.get('categoryPic',instance.productPic);
        instance.quantity = validated_data.get('quantity',instance.quantity);
        instance.categoryId = validated_data.get('categoryId',instance.categoryId);
        instance.avgRating = validated_data.get('avgRating',instance.avgRating);
        instance.price = validated_data.get('price',instance.price);
        instance.save();
        return instance;

    def validate_name(self,value):
        if  not re.search("[a-zA-Z]+", value):
            raise serializers.ValidationError("Field must contain only at least one alphabetic characters");
        else:
            return value
        
    def validate_productPic(self,value):
        return validate_picture(value);