from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from user_app.api.views import *

router = DefaultRouter()
router.register('', AddressViewSet, basename='address')

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user/address/', include(router.urls)),
]