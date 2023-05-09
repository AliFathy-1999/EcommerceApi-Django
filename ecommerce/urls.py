from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from user_app.api.views import AddressViewSet
from card_app.api.views import CartList, CartDetail
router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product_app.api.urls')),
    path('account/', include('user_app.api.urls')),
    path('user/', include(router.urls)),
    path('cart/', CartList.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
]


