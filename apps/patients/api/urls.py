from django.urls import path

from .views import (
    PatientCreateAPIView,
    PatientListAPIView,
    PatientRetrieveAPIView,
    PatientUpdateAPIView,
    PatientDeleteAPIView,
)


urlpatterns = [
    path("", PatientListAPIView.as_view(), name="patient-list"),

    path("create/", PatientCreateAPIView.as_view(), name="patient-create"),

    path("<int:pk>/", PatientRetrieveAPIView.as_view(), name="patient-detail"),

    path("<int:pk>/update/", PatientUpdateAPIView.as_view(), name="patient-update"),

    path("<int:pk>/delete/", PatientDeleteAPIView.as_view(), name="patient-delete"),
]