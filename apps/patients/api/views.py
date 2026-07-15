from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import User
from apps.patients.models import Patient
from .serializers import PatientSerializer


@extend_schema(
    tags=["Patients"],
    summary="Create Patient",
)
class PatientCreateAPIView(generics.CreateAPIView):

    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.RECEPTIONIST:
            return Response(
                {
                    "message": "Only receptionists can create patients."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Patient created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Patients"],
    summary="List Patients",
)
class PatientListAPIView(generics.ListAPIView):

    queryset = Patient.objects.all()

    serializer_class = PatientSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Patients"],
    summary="Patient Details",
)
class PatientRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Patient.objects.all()

    serializer_class = PatientSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Patients"],
    summary="Update Patient",
)
class PatientUpdateAPIView(generics.UpdateAPIView):

    queryset = Patient.objects.all()

    serializer_class = PatientSerializer

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
                "message": "Patient updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Patients"],
    summary="Delete Patient",
)
class PatientDeleteAPIView(generics.DestroyAPIView):

    queryset = Patient.objects.all()

    serializer_class = PatientSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        patient = self.get_object()

        patient.delete()

        return Response(
            {
                "message": "Patient deleted successfully."
            },
            status=status.HTTP_200_OK
        )