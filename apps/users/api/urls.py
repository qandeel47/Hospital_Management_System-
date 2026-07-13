from django.urls import path
from .views import ForgotPasswordAPIView, LogoutAPIView, RegisterAPIView, ResetPasswordAPIView
from .views import (RegisterAPIView, LoginAPIView,  MeAPIView, ChangePasswordAPIView,LogoutAPIView,
ForgotPasswordSerializer,ResetPasswordSerializer,)
urlpatterns = [

    path("register/",RegisterAPIView.as_view(),name="register",),
    path("login/",LoginAPIView.as_view(),name="login",),
    path("me/",MeAPIView.as_view(),name="me",),
    path("change-password/",ChangePasswordAPIView.as_view(),name="change-password",),
    path("logout/",LogoutAPIView.as_view(),name="logout",),
    path("forgot-password/",ForgotPasswordAPIView.as_view(),name="forgot-password",),
    path("reset-password/",ResetPasswordAPIView.as_view(),name="reset-password",),




]