from django.contrib import admin
from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "department",
        "specialization",
        "experience_years",
        "consultation_fee",
        "status",
    )

    list_filter = ("department", "status",)
    search_fields = ("user__username","user__email", "specialization",)
    ordering = ("user__username",)