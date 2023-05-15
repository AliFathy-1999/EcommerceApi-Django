from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import os
from user_app.api.serializers import RegistrationSerializer
from user_app import models
from user_app.api.serializers import AddressSerializer
from user_app.models import Address
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from card_app.models import Cart

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        user = request.user
        
        user.auth_token.delete()
        
        # delete user's profile picture from disk
        try:
            if user.profile_pic:
                profile_pic_path = os.path.join(settings.STATICFILES_DIRS[0], user.profile_pic)
                if os.path.exists(profile_pic_path):
                    os.remove(profile_pic_path)
        except AttributeError:
            pass
        
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
            cart = Cart(user=account)
            cart.save()
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
    
    
    
class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        """
        Return only the addresses for the authenticated user.
        """
        return Address.objects.filter(user=self.request.user)
    
    def get_object(self):
        """
        Get the address object for the specified id.
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        address = self.get_object()
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        address = self.get_object()
        address.delete()
        return Response({'success':'Address deleted successfuly'},status=status.HTTP_204_NO_CONTENT)