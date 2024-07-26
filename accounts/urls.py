from rest_framework_simplejwt.views import  TokenObtainPairView, TokenRefreshView
from django.urls import path

from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name='token_obtain_pair'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
