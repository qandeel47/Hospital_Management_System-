from django.contrib import admin
from .models import MedicalRecord


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):

    list_display = (
        "appointment",
        "doctor",
        "diagnosis",
        "created_at",
    )

    list_filter = (
        "doctor",
        "created_at",
    )

    search_fields = (
        "appointment__patient__patient_id",
        "appointment__patient__first_name",
        "appointment__patient__last_name",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "diagnosis",
    )

    ordering = (
        "-created_at",
    )