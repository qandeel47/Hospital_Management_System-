from django.db import models


class Department(models.Model):

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    name = models.CharField( max_length=100,unique=True)
    code = models.CharField(max_length=10,unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,choices=StatusChoices.choices,default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name