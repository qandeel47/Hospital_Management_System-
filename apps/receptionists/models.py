from django.db import models
from django.db import models

from apps.users.models import User
from apps.departments.models import Department


class Receptionist(models.Model):

    class ShiftChoices(models.TextChoices):
        MORNING = "MORNING", "Morning"
        EVENING = "EVENING", "Evening"
        NIGHT = "NIGHT", "Night"

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    user = models.OneToOneField( User,on_delete=models.CASCADE,related_name="receptionist_profile")
    department = models.ForeignKey(Department,on_delete=models.PROTECT,related_name="receptionists")
    shift = models.CharField(max_length=20,choices=ShiftChoices.choices)
    joining_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )

    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username