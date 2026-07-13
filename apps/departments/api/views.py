from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.departments.models import Department
from .serializers import DepartmentSerializer


@extend_schema(
    tags=["Departments"],
    summary="Create Department",
)
class DepartmentCreateAPIView(generics.CreateAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Department created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Departments"],
    summary="List Departments",
)
class DepartmentListAPIView(generics.ListAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Departments"],
    summary="Department Details",
)
class DepartmentRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Departments"],
    summary="Update Department",
)
class DepartmentUpdateAPIView(generics.UpdateAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
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
                "message": "Department updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Departments"],
    summary="Delete Department",
)
class DepartmentDeleteAPIView(generics.DestroyAPIView):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "message": "Department deleted successfully."
            },
            status=status.HTTP_200_OK
        )