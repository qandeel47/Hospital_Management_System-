from drf_spectacular.utils import extend_schema

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.billing.models import Billing
from apps.users.models import User

from .serializers import BillingSerializer


@extend_schema(
    tags=["Billing"],
    summary="Create Bill",
)
class BillingCreateAPIView(generics.CreateAPIView):

    serializer_class = BillingSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != User.RoleChoices.RECEPTIONIST:
            return Response(
                {
                    "message": "Only receptionists can create bills."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Bill created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Billing"],
    summary="List Bills",
)
class BillingListAPIView(generics.ListAPIView):

    queryset = Billing.objects.all()

    serializer_class = BillingSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Billing"],
    summary="Bill Details",
)
class BillingRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Billing.objects.all()

    serializer_class = BillingSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Billing"],
    summary="Update Bill",
)
class BillingUpdateAPIView(generics.UpdateAPIView):

    queryset = Billing.objects.all()

    serializer_class = BillingSerializer

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
                "message": "Bill updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Billing"],
    summary="Delete Bill",
)
class BillingDeleteAPIView(generics.DestroyAPIView):

    queryset = Billing.objects.all()

    serializer_class = BillingSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        bill = self.get_object()

        bill.delete()

        return Response(
            {
                "message": "Bill deleted successfully."
            },
            status=status.HTTP_200_OK,
        )