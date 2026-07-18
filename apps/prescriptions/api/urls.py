from django.urls import path

from .views import (
    PrescriptionCreateAPIView,
    PrescriptionListAPIView,
    PrescriptionRetrieveAPIView,
    PrescriptionUpdateAPIView,
    PrescriptionDeleteAPIView,
)

urlpatterns = [

    path(
        "create/",
        PrescriptionCreateAPIView.as_view(),
        name="prescription-create",
    ),

    path(
        "",
        PrescriptionListAPIView.as_view(),
        name="prescription-list",
    ),

    path(
        "<int:pk>/",
        PrescriptionRetrieveAPIView.as_view(),
        name="prescription-detail",
    ),

    path(
        "<int:pk>/update/",
        PrescriptionUpdateAPIView.as_view(),
        name="prescription-update",
    ),

    path(
        "<int:pk>/delete/",
        PrescriptionDeleteAPIView.as_view(),
        name="prescription-delete",
    ),

]