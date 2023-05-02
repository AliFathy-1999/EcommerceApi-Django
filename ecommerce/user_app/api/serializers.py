# from django.contrib.auth.models import User
from user_app.models import User
from rest_framework import serializers
import os

class RegistrationSerializer(serializers.ModelSerializer):
    
    # firstName = serializers.CharField(min_length=3,max_length=20)
    # lastName = serializers.CharField(min_length=3,max_length=20)
    # profilePic = serializers.ImageField()
    
    class Meta:
        model = User
        fields = ('id','firstName','lastName','username','email','password','profilePic')
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
        
    def validate_profilePic(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.jpeg', '.png','.jfif','.jpg']
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError("File extension not supported. Supported extensions are .png, .jpeg, .jpg, .jfif.")
        
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size exceeds the limit of 5 MB.")
        
        return value
    
    def save(self):
        
        password=self.validated_data['password']
        profilePic = self.validated_data.get('profilePic')
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'username already exists!'})
        
        account = User(
                firstName=self.validated_data['firstName'], 
                lastName=self.validated_data['lastName'],
                email=self.validated_data['email'],
                username=self.validated_data['username'],
            )
        
        account.set_password(password)
        
        if profilePic:
            account.profilePic = profilePic
            
        account.save()
        
        return account
        
        
        
        
    