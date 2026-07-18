from django.db import models
from apps.medical_records.models import MedicalRecord
from apps.doctors.models import Doctor


class Prescription(models.Model):
    medical_record = models.OneToOneField(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name="prescription",
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )

    medicines = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Prescription - "
            f"{self.medical_record.appointment.patient.patient_id}"
        )