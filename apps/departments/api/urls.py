from django.urls import path
from .views import (
    DepartmentCreateAPIView,
    DepartmentListAPIView,
    DepartmentRetrieveAPIView,
    DepartmentUpdateAPIView,
    DepartmentDeleteAPIView,
)

urlpatterns = [
    path(
        "",
        DepartmentListAPIView.as_view(),
        name="department-list",
    ),
    path(
        "create/",
        DepartmentCreateAPIView.as_view(),
        name="department-create",
    ),
    path(
        "<int:pk>/",
        DepartmentRetrieveAPIView.as_view(),
        name="department-detail",
    ),
    path(
        "<int:pk>/update/",
        DepartmentUpdateAPIView.as_view(),
        name="department-update",
    ),
    path(
        "<int:pk>/delete/",
        DepartmentDeleteAPIView.as_view(),
        name="department-delete",
    ),
]