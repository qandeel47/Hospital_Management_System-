from django.urls import path

from .views import (
    AppointmentCreateAPIView,
    AppointmentListAPIView,
    AppointmentRetrieveAPIView,
    AppointmentUpdateAPIView,
    AppointmentDeleteAPIView,
)

urlpatterns = [

    path(
        "create/",
        AppointmentCreateAPIView.as_view(),
        name="appointment-create",
    ),

    path(
        "",
        AppointmentListAPIView.as_view(),
        name="appointment-list",
    ),

    path(
        "<int:pk>/",
        AppointmentRetrieveAPIView.as_view(),
        name="appointment-detail",
    ),

    path(
        "<int:pk>/update/",
        AppointmentUpdateAPIView.as_view(),
        name="appointment-update",
    ),

    path(
        "<int:pk>/delete/",
        AppointmentDeleteAPIView.as_view(),
        name="appointment-delete",
    ),

]