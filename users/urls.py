# urls.py
from django.urls import path

from .views import UserLoginAPIView, UserSignUpAPIView

urlpatterns = [
    path("signup/", UserSignUpAPIView.as_view(), name="user-signup"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
]
