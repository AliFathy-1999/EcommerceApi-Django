"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product_app.api.urls')),
=======
from rest_framework import routers
from user_app.api.views import AddressViewSet

router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user_app.api.urls')),
     path('user/', include(router.urls)),
>>>>>>> 4f6d5125dbc26c3d034f640b5bd94d8afe65ccdb
]
