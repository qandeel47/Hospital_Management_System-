from rest_framework import serializers
from apps.receptionists.models import Receptionist
from apps.departments.models import Department


class ReceptionistSerializer(serializers.ModelSerializer):

    department = serializers.CharField(write_only=True)

    class Meta:
        model = Receptionist

        fields = (
            "department",
            "shift",
            "joining_date",
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

        receptionist = Receptionist.objects.create(
            user=self.context["request"].user,
            department=department,
            **validated_data
        )

        return receptionist