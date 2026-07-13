from attr import attrs
from rest_framework import serializers
from apps.users.models import User, HospitalID
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes,force_str
from django.utils.http import( urlsafe_base64_encode,urlsafe_base64_decode,)
from django.core.mail import send_mail

class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)
    hospital_id = serializers.CharField(write_only=True)

    role = serializers.ChoiceField(
        choices=[
            User.RoleChoices.DOCTOR,
            User.RoleChoices.RECEPTIONIST,
        ]
    )

    class Meta:
        model = User

        fields = (
            "role",
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
        role = attrs.get("role")

        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

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

        if hospital.role != role:
            raise serializers.ValidationError(
                {
                    "hospital_id": "Hospital ID does not belong to the selected role."
                }
            )

        if hospital.status != HospitalID.StatusChoices.ACTIVE:
            raise serializers.ValidationError(
                {
                    "hospital_id": "This Hospital ID is inactive. Please contact the administrator."
                }
            )

        if hospital.is_registered:
            raise serializers.ValidationError(
                {
                    "hospital_id": "This Hospital ID has already been registered."
                }
            )

        attrs["hospital"] = hospital

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")
        validated_data.pop("hospital_id")

        hospital = validated_data.pop("hospital")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data["phone_number"],
            gender=validated_data["gender"],
            role=validated_data["role"],
            hospital_id=hospital,
        )

        hospital.is_registered = True
        hospital.save()

        return user
    
class LoginSerializer(serializers.Serializer):

    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        # Check whether user entered email or username
        if "@" in username_or_email:

            try:
                user = User.objects.get(
                    email=username_or_email
                )
                username = user.username

            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "username_or_email": "Invalid username/email or password."
                    }
                )

        else:
            username = username_or_email

        # Authenticate user
        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                {
                    "username_or_email": "Invalid username/email or password."
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "username_or_email": "This account is inactive."
                }
            )

        # Save user object for use later
        attrs["user"] = user

        return attrs

    def create(self, validated_data):

        user = validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }
    

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "gender",
            "role",
            "profile_picture",
            "created_at",
        )

        read_only_fields = fields


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        user = self.context["request"].user

        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        # Check current password
        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {
                    "current_password": "Current password is incorrect."
                }
            )

        # Check new password confirmation
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        return attrs

    def save(self, **kwargs):

        user = self.context["request"].user

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        return user
    

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def save(self, **kwargs):

        refresh_token = self.validated_data["refresh"]

        token = RefreshToken(refresh_token)

        token.blacklist()


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No account found with this email."
            )

        return value

    def save(self):

        email = self.validated_data["email"]

        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = (
            f"http://localhost:8000/api/users/reset-password/"
            f"?uid={uid}&token={token}"
        )

        send_mail(
            subject="Hospital Management System Password Reset",
            message=(
                f"Hello {user.username},\n\n"
                f"Click the link below to reset your password:\n\n"
                f"{reset_link}"
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )


class ResetPasswordSerializer(serializers.Serializer):

    uid = serializers.CharField()

    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        try:

            uid = force_str(
                urlsafe_base64_decode(attrs["uid"])
            )

            user = User.objects.get(pk=uid)

        except Exception:

            raise serializers.ValidationError(
                {
                    "uid": "Invalid user."
                }
            )

        if not PasswordResetTokenGenerator().check_token(
            user,
            attrs["token"]
        ):

            raise serializers.ValidationError(
                {
                    "token": "Invalid or expired token."
                }
            )

        attrs["user"] = user

        return attrs

    def save(self):

        user = self.validated_data["user"]

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        return user