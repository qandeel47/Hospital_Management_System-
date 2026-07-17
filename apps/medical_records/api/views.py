from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.medical_records.models import MedicalRecord
from apps.users.models import User
from .serializers import MedicalRecordSerializer


@extend_schema(
    tags=["Medical Records"],
    summary="Create Medical Record",
)
class MedicalRecordCreateAPIView(generics.CreateAPIView):

    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.DOCTOR:
            return Response(
                {
                    "message": "Only doctors can create medical records."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Medical record created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Medical Records"],
    summary="List Medical Records",
)
class MedicalRecordListAPIView(generics.ListAPIView):

    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Medical Records"],
    summary="Medical Record Details",
)
class MedicalRecordRetrieveAPIView(generics.RetrieveAPIView):

    queryset = MedicalRecord.objects.all()

    serializer_class = MedicalRecordSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Medical Records"],
    summary="Update Medical Record",
)
class MedicalRecordUpdateAPIView(generics.UpdateAPIView):

    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
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
                "message": "Medical record updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Medical Records"],
    summary="Delete Medical Record",
)
class MedicalRecordDeleteAPIView(generics.DestroyAPIView):

    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):

        medical_record = self.get_object()

        medical_record.delete()

        return Response(
            {
                "message": "Medical record deleted successfully."
            },
            status=status.HTTP_200_OK,
        )