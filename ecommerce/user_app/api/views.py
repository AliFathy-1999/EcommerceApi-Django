from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
import os
from user_app.api.serializers import RegistrationSerializer
from user_app import models


@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        user = request.user
        user.auth_token.delete()
        
        # delete user's profile picture from disk
        if user.profile_pic:
            profile_pic_path = os.path.join(settings.STATICFILES_DIRS[0], user.profile_pic)
            if os.path.exists(profile_pic_path):
                os.remove(profile_pic_path)
        
        user.delete()
        return Response({'success':'logged out successfuly'},status=status.HTTP_200_OK)


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['profile_pic'] = account.profile_pic
            token = Token.objects.get(user=account).key
            data['token'] = token
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)