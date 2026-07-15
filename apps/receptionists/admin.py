from django.contrib import admin

from .models import Receptionist


@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "department",
        "shift",
        "status",
        "joining_date",
    )

    list_filter = (
        "department",
        "shift",
        "status",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__hospital_id__hospital_id",
    )

    ordering = (
        "user__username",
    )