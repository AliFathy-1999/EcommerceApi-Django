from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True,min_length=4,max_length=20)
    last_name = serializers.CharField(required=True,min_length=4,max_length=20)
    profile_pic = serializers.ImageField(required=True)
    username = serializers.CharField(required=True,min_length=4, max_length=20)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name','last_name','profile_pic']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    def validate_profile_pic(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.jpeg', '.png','.jfif','.jpg']
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError("File extension not supported. Supported extensions are .png, .jpeg, .jpg, .jfif.")
        
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size exceeds the limit of 5 MB.")
        
        return value
    
    def validate_first_name_last_name(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if not isinstance(first_name, str):
            raise serializers.ValidationError("First name must be a string.")
        
        if not isinstance(last_name, str):
            raise serializers.ValidationError("Last name must be a string.")
        
        if len(first_name) < 4 or len(first_name) > 20:
            raise serializers.ValidationError("First name length must be between 4 and 20 characters.")
        
        if len(last_name) < 4 or len(last_name) > 20:
            raise serializers.ValidationError("Last name length must be between 4 and 20 characters.")
        
        return data
    
    def validate_username(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Username must be a string.")
        
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError("Username length must be between 4 and 20 characters.")
        
        return value
    
    
    
    def save(self):

        password = self.validated_data['password']
        profile_pic = self.validated_data['profile_pic']
        
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'username already exists!'})
        

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name = self.validated_data['last_name'],

            )
        
        user.set_password(password)
            
        user.save()
        
        # Set the profile_pic attribute on the user instance directly
        # fs = FileSystemStorage()
        # filename = fs.save(profile_pic.name, ContentFile(profile_pic.read()))
        # user.profile_pic = filename
        # user.save()
        
        filename = str(self.validated_data['username']) + os.path.splitext(self.validated_data['profile_pic'].name)[1]

        # create a FileSystemStorage instance for the static directory
        fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])

        # save the image to the static directory
        fs.save(filename, self.validated_data['profile_pic'])
        
        # profile_pic = User(user=account, profile_pic=filename)
        # profile_pic.save()
        
        user.profile_pic = filename
        user.save()

        return user
        
    