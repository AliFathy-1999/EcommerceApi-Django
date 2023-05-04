from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from product_app.models import Category
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(min_length=3,max_length=40)
    categoryPic = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], required=False)
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data);
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.categoryPic = validated_data.get('categoryPic',instance.categoryPic)
        instance.save();
        return instance;
    