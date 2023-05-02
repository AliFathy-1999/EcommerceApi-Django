# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view, permission_classes
# from user_app.api.serializers import RegistrationSerializer
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.contrib.auth import authenticate, login
# from user_app import models

# @login_required
# @api_view(['POST',])
# def logout_view(request):
#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)
    
    
# @csrf_exempt
# @api_view(['POST',])
# @permission_classes([AllowAny])
# def registration_view(request):

#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
        
#         data = {}
        
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = "Registration Successful!"
#             data['firstName'] = account.firstName
#             data['lastName'] = account.lastName
#             data['profilePic'] = account.profilePic
#             data['username'] = account.username
#             data['email'] = account.email
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data = serializer.errors
        
#         return Response(data, status=status.HTTP_201_CREATED)
    
   
# # @csrf_exempt
# # @api_view(['POST'])
# # @permission_classes([AllowAny])
# # def login_view(request):
# #     username = request.POST.get('username')
# #     password = request.POST.get('password')
# #     user = authenticate(request, username=username, password=password)
# #     if user is not None:
# #         login(request, user)
# #         token, created = Token.objects.get_or_create(user=user)
# #         return JsonResponse({'token': token.key})
# #     return JsonResponse({'error': 'Invalid credentials'}, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

from user_app.api.serializers import RegistrationSerializer
from user_app import models


@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


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
            data['firstName'] = account.firstName
            data['lastName'] = account.lastName
            data['profilePicture'] = account.profilePicture
            token = Token.objects.get(user=account).key
            data['token'] = token
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)