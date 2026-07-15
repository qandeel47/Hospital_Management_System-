from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import User
from apps.receptionists.models import Receptionist
from .serializers import ReceptionistSerializer


@extend_schema(
    tags=["Receptionists"],
    summary="Create Receptionist Profile",
)
class ReceptionistCreateAPIView(generics.CreateAPIView):

    serializer_class = ReceptionistSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.RECEPTIONIST:
            return Response(
                {
                    "message": "Only receptionists can create a profile."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if Receptionist.objects.filter(user=request.user).exists():
            return Response(
                {
                    "message": "Receptionist profile already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Receptionist profile created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Receptionists"],
    summary="List Receptionists",
)
class ReceptionistListAPIView(generics.ListAPIView):

    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Receptionists"],
    summary="Receptionist Details",
)
class ReceptionistRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Receptionists"],
    summary="Update Receptionist",
)
class ReceptionistUpdateAPIView(generics.UpdateAPIView):

    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer
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
                "message": "Receptionist updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Receptionists"],
    summary="Delete Receptionist",
)
class ReceptionistDeleteAPIView(generics.DestroyAPIView):

    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        receptionist = self.get_object()
        receptionist.delete()

        return Response(
            {
                "message": "Receptionist deleted successfully."
            },
            status=status.HTTP_200_OK
        )