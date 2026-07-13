from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import (RegisterSerializer,LoginSerializer,UserProfileSerializer, ChangePasswordSerializer,
 LogoutSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,)


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        tags=["Users"],
        summary="Register Doctor or Receptionist",
        description="Register a doctor or receptionist using a valid Hospital ID.",
    )
    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Registration successful."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        tags=["Users"],
        summary="User Login",
        description="Login using username or email and password.",
    )
    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            data = serializer.save()

            return Response(
                data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Users"],
        summary="Current User",
        description="Return the profile of the currently authenticated user.",
        responses=UserProfileSerializer,
    )
    def get(self, request):

        serializer = UserProfileSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        tags=["Users"],
        summary="Change Password",
        description="Change the password of the authenticated user.",
    )
    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Password changed successfully."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=LogoutSerializer,
        tags=["Users"],
        summary="Logout"
    )
    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Logout successful."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class ForgotPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        tags=["Users"],
        summary="Forgot Password",
    )
    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Password reset link sent successfully."
            },
            status=status.HTTP_200_OK,
        )
    

class ResetPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        tags=["Users"],
        summary="Reset Password",
    )
    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Password reset successfully."
            },
            status=status.HTTP_200_OK,
        )