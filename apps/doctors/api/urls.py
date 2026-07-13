from django.urls import path

from .views import (
    DoctorCreateAPIView,
    DoctorListAPIView,
    DoctorRetrieveAPIView,
    DoctorUpdateAPIView,
    DoctorDeleteAPIView,
)

urlpatterns = [
    path("", DoctorListAPIView.as_view(), name="doctor-list"),
    path("create/", DoctorCreateAPIView.as_view(), name="doctor-create"),
    path("<int:pk>/", DoctorRetrieveAPIView.as_view(), name="doctor-detail"),
    path("<int:pk>/update/", DoctorUpdateAPIView.as_view(), name="doctor-update"),
    path("<int:pk>/delete/", DoctorDeleteAPIView.as_view(), name="doctor-delete"),
]