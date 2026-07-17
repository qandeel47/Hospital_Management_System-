from datetime import date
from rest_framework import serializers
from apps.appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment

        fields = (
            "id",
            "patient",
            "doctor",
            "appointment_date",
            "appointment_time",
            "reason",
            "status",
            "created_at",
        )

        read_only_fields = (
            "status",
            "created_at",
        )

    def validate(self, attrs):

        appointment_date = attrs.get("appointment_date")
        appointment_time = attrs.get("appointment_time")
        doctor = attrs.get("doctor")

        if appointment_date < date.today():
            raise serializers.ValidationError(
                {
                    "appointment_date": "Appointment date cannot be in the past."
                }
            )

        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ).exists():
            raise serializers.ValidationError(
                {
                    "appointment_time": "This doctor already has an appointment at this time."
                }
            )

        return attrs

    def create(self, validated_data):

        appointment = Appointment.objects.create(
            created_by=self.context["request"].user,
            **validated_data
        )

        return appointment