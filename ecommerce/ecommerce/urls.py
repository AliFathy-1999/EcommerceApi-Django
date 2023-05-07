
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from user_app.api.views import AddressViewSet

router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product_app.api.urls')),
    path('account/', include('user_app.api.urls')),
    path('user/', include(router.urls)),
]


