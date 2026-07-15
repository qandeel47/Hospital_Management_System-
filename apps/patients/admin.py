from django.contrib import admin
from .models import Patient
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        "patient_id",
        "first_name",
        "last_name",
        "phone_number",
        "gender",
        "blood_group",
        "created_by",
    )

    list_filter = (
        "gender",
 
        "blood_group",
    )

    search_fields = (
        "patient_id",
        "first_name",
        "last_name",
        "phone_number",
        "email",
    )

    ordering = (
        "patient_id",
    )