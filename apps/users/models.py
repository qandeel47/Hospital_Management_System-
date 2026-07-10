from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser

class HospitalID(models.Model):

    class RoleChoices(models.TextChoices):
        DOCTOR = "DOCTOR", "Doctor"
        RECEPTIONIST = "RECEPTIONIST", "Receptionist"

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    hospital_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField( max_length=150)
    role = models.CharField(max_length=20,choices=RoleChoices.choices)    

    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )

    is_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hospital_id} - {self.full_name}"



class User(AbstractUser):

    objects = UserManager()

    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    class RoleChoices(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DOCTOR = "DOCTOR", "Doctor"
        RECEPTIONIST = "RECEPTIONIST", "Receptionist"
        PATIENT = "PATIENT", "Patient"

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField( max_length=10,choices=GenderChoices.choices)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices
    )

    hospital_id = models.OneToOneField(
        HospitalID,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username