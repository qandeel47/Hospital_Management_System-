from django.contrib import admin
from .models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = (
        "medical_record",
        "doctor",
        "created_at",
    )

    list_filter = (
        "doctor",
        "created_at",
    )

    search_fields = (
        "medical_record__appointment__patient__patient_id",
        "medical_record__appointment__patient__first_name",
        "medical_record__appointment__patient__last_name",
        "doctor__user__first_name",
        "doctor__user__last_name",
    )

    ordering = (
        "-created_at",
    )