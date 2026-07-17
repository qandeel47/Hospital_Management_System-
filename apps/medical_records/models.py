from django.db import models
from apps.appointments.models import Appointment
from apps.doctors.models import Doctor


class MedicalRecord(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="medical_record",
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="medical_records",
    )
    diagnosis = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.appointment.patient.patient_id} - {self.diagnosis}"