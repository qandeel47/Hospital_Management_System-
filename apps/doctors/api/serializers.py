from rest_framework import serializers

from apps.doctors.models import Doctor
from apps.departments.models import Department


class DoctorSerializer(serializers.ModelSerializer):

    department = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor

        fields = (
            "department",
            "specialization",
            "qualification",
            "experience_years",
            "consultation_fee",
            "joining_date",
            "bio",
            "status",
        )

    def validate_department(self, value):

        try:
            department = Department.objects.get(
                name__iexact=value
            )
        except Department.DoesNotExist:
            raise serializers.ValidationError(
                "Department not found."
            )

        return department

    def create(self, validated_data):

        department = validated_data.pop("department")

        doctor = Doctor.objects.create(
            user=self.context["request"].user,
            department=department,
            **validated_data
        )

        return doctor