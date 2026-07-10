from django.urls import path

from .views import DoctorRegistrationAPIView

urlpatterns = [
    path(
        "doctors/register/",
        DoctorRegistrationAPIView.as_view(),
        name="doctor-register",
    ),
]