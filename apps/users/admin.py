from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, HospitalID


@admin.register(HospitalID)
class HospitalIDAdmin(admin.ModelAdmin):
    list_display = (
        "hospital_id",
        "full_name",
        "role",
        "status",
        "is_registered",
    )

    list_filter = (
        "role",
        "status",
        "is_registered",
    )

    search_fields = (
        "hospital_id",
        "full_name",
    )


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "role",
        "phone_number",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "email",
        "phone_number",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Hospital Information",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "gender",
                    "hospital_id",
                    "profile_picture",
                )
            },
        ),
    )