# # from django.contrib.auth.models import User
# from user_app.models import User
# from rest_framework import serializers
# import os

# class RegistrationSerializer(serializers.ModelSerializer):
    
#     # firstName = serializers.CharField(min_length=3,max_length=20)
#     # lastName = serializers.CharField(min_length=3,max_length=20)
#     # profilePic = serializers.ImageField()
    
#     class Meta:
#         model = User
#         fields = ('id','firstName','lastName','username','email','password','profilePic')
#         extra_kwargs = {
#             'password' : {'write_only': True}
#         }
        
        
#     def validate_profilePic(self, value):
#         ext = os.path.splitext(value.name)[1]
#         valid_extensions = ['.jpg', '.jpeg', '.png','.jfif','.jpg']
#         if not ext.lower() in valid_extensions:
#             raise serializers.ValidationError("File extension not supported. Supported extensions are .png, .jpeg, .jpg, .jfif.")
        
#         max_size = 5 * 1024 * 1024
#         if value.size > max_size:
#             raise serializers.ValidationError("File size exceeds the limit of 5 MB.")
        
#         return value
    
#     def save(self):
        
#         password=self.validated_data['password']
#         profilePic = self.validated_data.get('profilePic')
        
#         if User.objects.filter(email=self.validated_data['email']).exists():
#             raise serializers.ValidationError({'error': 'Email already exists!'})
        
#         if User.objects.filter(username=self.validated_data['username']).exists():
#             raise serializers.ValidationError({'error': 'username already exists!'})
        
#         account = User(
#                 firstName=self.validated_data['firstName'], 
#                 lastName=self.validated_data['lastName'],
#                 email=self.validated_data['email'],
#                 username=self.validated_data['username'],
#             )
        
#         account.set_password(password)
        
#         if profilePic:
#             account.profilePic = profilePic
            
#         account.save()
        
#         return account
        
from django.contrib.auth.models import User
from rest_framework import serializers
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

class RegistrationSerializer(serializers.ModelSerializer):
    
    firstName = serializers.CharField(required=True,min_length=4,max_length=20)
    lastName = serializers.CharField(required=True,min_length=4,max_length=20)
    profilePic = serializers.ImageField(required=True)
    username = serializers.CharField(required=True,min_length=4, max_length=20)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'firstName','lastName','profilePic']
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
    
    def validate_firstName_lastName(self, data):
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        
        if not isinstance(firstName, str):
            raise serializers.ValidationError("First name must be a string.")
        
        if not isinstance(lastName, str):
            raise serializers.ValidationError("Last name must be a string.")
        
        if len(firstName) < 4 or len(firstName) > 20:
            raise serializers.ValidationError("First name length must be between 4 and 20 characters.")
        
        if len(lastName) < 4 or len(lastName) > 20:
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
        
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'username': 'Email already exists!'})
        

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        filename = self.validated_data['username'] + os.path.splitext(self.validated_data['profilePic'])[1]
        # create a FileSystemStorage instance for the static directory
        fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])

        # save the image to the static directory
        fs.save(filename, self.validated_data['profilePic'])
        
        account = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
                firstName=self.validated_data['firstName'],
                lastName = self.validated_data['lastName'],
                profilePic = filename,
            )
        
        account.set_password(password)
            
        account.save()

        return account
        
    