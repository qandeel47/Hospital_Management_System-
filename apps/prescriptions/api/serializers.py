from rest_framework import serializers
from apps.doctors.models import Doctor
from apps.medical_records.models import MedicalRecord
from apps.prescriptions.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription

        fields = (
            "id",
            "medical_record",
            "medicines",
            "dosage",
            "instructions",
            "created_at",
        )

        read_only_fields = (
            "created_at",
        )

    def validate(self, attrs):

        medical_record = attrs.get("medical_record")
        request = self.context["request"]

        try:
            doctor = Doctor.objects.get(user=request.user)

        except Doctor.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "doctor": "Doctor profile not found."
                }
            )

        if medical_record.doctor != doctor:
            raise serializers.ValidationError(
                {
                    "medical_record": "You can only create prescriptions for your own medical records."
                }
            )

        if Prescription.objects.filter(
            medical_record=medical_record
        ).exists():
            raise serializers.ValidationError(
                {
                    "medical_record": "Prescription already exists for this medical record."
                }
            )

        return attrs

    def create(self, validated_data):

        doctor = Doctor.objects.get(
            user=self.context["request"].user
        )

        prescription = Prescription.objects.create(
            doctor=doctor,
            **validated_data
        )

        return prescription