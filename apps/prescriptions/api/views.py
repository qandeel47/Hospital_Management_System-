from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.prescriptions.models import Prescription
from apps.users.models import User
from .serializers import PrescriptionSerializer


@extend_schema(
    tags=["Prescriptions"],
    summary="Create Prescription",
)
class PrescriptionCreateAPIView(generics.CreateAPIView):

    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.DOCTOR:
            return Response(
                {
                    "message": "Only doctors can create prescriptions."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Prescription created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Prescriptions"],
    summary="List Prescriptions",
)
class PrescriptionListAPIView(generics.ListAPIView):

    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Prescriptions"],
    summary="Prescription Details",
)
class PrescriptionRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Prescriptions"],
    summary="Update Prescription",
)
class PrescriptionUpdateAPIView(generics.UpdateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
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
                "message": "Prescription updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Prescriptions"],
    summary="Delete Prescription",
)
class PrescriptionDeleteAPIView(generics.DestroyAPIView):

    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        prescription = self.get_object()
        prescription.delete()
        return Response(
            {
                "message": "Prescription deleted successfully."
            },
            status=status.HTTP_200_OK,
        )