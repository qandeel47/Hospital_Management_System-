from rest_framework import serializers

from apps.users.models import User, HospitalID


class DoctorRegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)
    hospital_id = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "password",
            "confirm_password",
            "phone_number",
            "gender",
            "hospital_id",
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        hospital_id = attrs.get("hospital_id")

        # Check password and confirm password
        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        # Check Hospital ID
        try:
            hospital = HospitalID.objects.get(
                hospital_id=hospital_id
            )

        except HospitalID.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "hospital_id": "Invalid Hospital ID."
                }
            )

        # Check role
        if hospital.role != HospitalID.RoleChoices.DOCTOR:
            raise serializers.ValidationError(
                {
                    "hospital_id": "This Hospital ID belongs to a Receptionist."
                }
            )

        # Check status
        if hospital.status != HospitalID.StatusChoices.ACTIVE:
            raise serializers.ValidationError(
                {
                    "hospital_id": "This Hospital ID is inactive. Please contact the administrator."
                }
            )

        # Check registration status
        if hospital.is_registered:
            raise serializers.ValidationError(
                {
                    "hospital_id": "This Hospital ID has already been registered."
                }
            )

        # Save Hospital object for create()
        attrs["hospital"] = hospital

        return attrs

    def create(self, validated_data):

        # Remove extra fields
        validated_data.pop("confirm_password")
        hospital = validated_data.pop("hospital")
        validated_data.pop("hospital_id")

        # Create User
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data["phone_number"],
            gender=validated_data["gender"],
            role = hospital.role,
            hospital_id=hospital,
        )

        # Update Hospital ID status
        hospital.is_registered = True
        hospital.save()

        return user