from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.appointments.models import Appointment
from apps.users.models import User
from .serializers import AppointmentSerializer


@extend_schema(
    tags=["Appointments"],
    summary="Create Appointment",
)
class AppointmentCreateAPIView(generics.CreateAPIView):

    serializer_class = AppointmentSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.RECEPTIONIST:
            return Response(
                {
                    "message": "Only receptionists can create appointments."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Appointment created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Appointments"],
    summary="List Appointments",
)
class AppointmentListAPIView(generics.ListAPIView):

    queryset = Appointment.objects.all()

    serializer_class = AppointmentSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Appointments"],
    summary="Appointment Details",
)
class AppointmentRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Appointment.objects.all()

    serializer_class = AppointmentSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Appointments"],
    summary="Update Appointment",
)
class AppointmentUpdateAPIView(generics.UpdateAPIView):

    queryset = Appointment.objects.all()

    serializer_class = AppointmentSerializer

    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            {
                "message": "Appointment updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Appointments"],
    summary="Delete Appointment",
)
class AppointmentDeleteAPIView(generics.DestroyAPIView):

    queryset = Appointment.objects.all()

    serializer_class = AppointmentSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        appointment = self.get_object()

        appointment.delete()

        return Response(
            {
                "message": "Appointment deleted successfully."
            },
            status=status.HTTP_200_OK,
        )