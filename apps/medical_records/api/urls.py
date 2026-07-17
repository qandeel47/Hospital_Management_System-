from django.urls import path

from .views import (
    MedicalRecordCreateAPIView,
    MedicalRecordListAPIView,
    MedicalRecordRetrieveAPIView,
    MedicalRecordUpdateAPIView,
    MedicalRecordDeleteAPIView,
)

urlpatterns = [

    path(
        "create/",
        MedicalRecordCreateAPIView.as_view(),
        name="medical-record-create",
    ),

    path(
        "",
        MedicalRecordListAPIView.as_view(),
        name="medical-record-list",
    ),

    path(
        "<int:pk>/",
        MedicalRecordRetrieveAPIView.as_view(),
        name="medical-record-detail",
    ),

    path(
        "<int:pk>/update/",
        MedicalRecordUpdateAPIView.as_view(),
        name="medical-record-update",
    ),

    path(
        "<int:pk>/delete/",
        MedicalRecordDeleteAPIView.as_view(),
        name="medical-record-delete",
    ),

]