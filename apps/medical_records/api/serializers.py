from rest_framework import serializers
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalRecord

        fields = (
            "id",
            "appointment",
            "diagnosis",
            "symptoms",
            "treatment",
            "notes",
            "created_at",
        )

        read_only_fields = (
            "created_at",
        )

    def validate(self, attrs):

        appointment = attrs.get("appointment")

        request = self.context["request"]

        try:
            doctor = Doctor.objects.get(user=request.user)

        except Doctor.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "doctor": "Doctor profile not found."
                }
            )

        if appointment.doctor != doctor:
            raise serializers.ValidationError(
                {
                    "appointment": "You can only create a medical record for your own appointments."
                }
            )

        if MedicalRecord.objects.filter(appointment=appointment).exists():
            raise serializers.ValidationError(
                {
                    "appointment": "Medical record already exists for this appointment."
                }
            )

        return attrs

    def create(self, validated_data):

        doctor = Doctor.objects.get(
            user=self.context["request"].user
        )

        medical_record = MedicalRecord.objects.create(
            doctor=doctor,
            **validated_data
        )

        return medical_record