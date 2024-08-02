from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("", TestApi.as_view(), name="test"),
    path("signup/", SignUpView.as_view(), name = "signup"),
    # path("login/", obtain_auth_token, name="login"),
    # path("logout/", LogOutView.as_view(), name="logout"),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
