from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "code",
        "status",
        "created_at",
    )

    list_filter = ( "status",)
    search_fields = ("name","code",)
    ordering = ("name",)