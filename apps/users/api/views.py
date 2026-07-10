from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .serializers import DoctorRegistrationSerializer


class DoctorRegistrationAPIView(APIView):

    @extend_schema(
        request=DoctorRegistrationSerializer,
        responses={
            201: {"description": "Doctor registered successfully."},
            400: {"description": "Validation Error"},
        },
        tags=["Users"],
        summary="Doctor Registration",
        description="Register a doctor using a valid Hospital ID.",
    )
    def post(self, request):

        serializer = DoctorRegistrationSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Doctor registered successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )