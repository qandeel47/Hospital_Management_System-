from rest_framework import serializers

from apps.patients.models import Patient
from apps.users.models import User


class PatientSerializer(serializers.ModelSerializer):

    age = serializers.ReadOnlyField()

    class Meta:
        model = Patient

        fields = (
            "patient_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "date_of_birth",
            "age",
            "weight",
            "blood_group",
            "address",
            "emergency_contact_name",
            "emergency_contact_number",
            "created_at",
        )

        read_only_fields = (
            "patient_id",
            "age",
            "created_at",
        )

    def create(self, validated_data):

        last_patient = Patient.objects.order_by("-id").first()

        if last_patient:
            last_id = int(last_patient.patient_id.split("-")[1]) + 1
        else:
            last_id = 1

        patient_id = f"PAT-{last_id:04d}"

        patient = Patient.objects.create(
            patient_id=patient_id,
            created_by=self.context["request"].user,
            **validated_data
        )

        return patient