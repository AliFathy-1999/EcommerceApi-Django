# from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
# from user_app.api.views import registration_view, logout_view

# app_name='user_app'

# urlpatterns = [
#     path('register/', registration_view, name='register'),
#     # path('login/', obtain_auth_token, name='login'),
#     path('logout/', logout_view, name='logout'),
# ]


from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user_app.api.views import registration_view, logout_view


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
]