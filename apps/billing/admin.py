from django.contrib import admin

from .models import Billing


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):

    list_display = (
        "appointment",
        "consultation_fee",
        "total_amount",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "created_at",
    )

    search_fields = (
        "appointment__patient__patient_id",
        "appointment__patient__first_name",
        "appointment__patient__last_name",
        "appointment__doctor__user__first_name",
        "appointment__doctor__user__last_name",
    )

    ordering = (
        "-created_at",
    )