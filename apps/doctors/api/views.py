from drf_spectacular.utils import extend_schema

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.doctors.models import Doctor

from .serializers import DoctorSerializer


@extend_schema(
    tags=["Doctors"],
    summary="Create Doctor Profile",
)
class DoctorCreateAPIView(generics.CreateAPIView):

    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.DOCTOR:
            return Response(
                {
                    "message": "Only doctors can create a profile."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if Doctor.objects.filter(user=request.user).exists():
            return Response(
                {
                    "message": "Doctor profile already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Doctor profile created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Doctors"],
    summary="List Doctors",
)
class DoctorListAPIView(generics.ListAPIView):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Doctors"],
    summary="Doctor Details",
)
class DoctorRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Doctors"],
    summary="Update Doctor",
)
class DoctorUpdateAPIView(generics.UpdateAPIView):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            {
                "message": "Doctor updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Doctors"],
    summary="Delete Doctor",
)
class DoctorDeleteAPIView(generics.DestroyAPIView):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        doctor = self.get_object()

        doctor.delete()

        return Response(
            {
                "message": "Doctor deleted successfully."
            },
            status=status.HTTP_200_OK
        )