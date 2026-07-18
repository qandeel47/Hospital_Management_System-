from decimal import Decimal

from rest_framework import serializers

from apps.appointments.models import Appointment
from apps.billing.models import Billing


class BillingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billing

        fields = (
            "id",
            "appointment",
            "consultation_fee",
            "medicine_charges",
            "test_charges",
            "discount",
            "total_amount",
            "payment_status",
            "created_at",
        )

        read_only_fields = (
            "consultation_fee",
            "total_amount",
            "created_at",
        )

    def validate(self, attrs):

        appointment = attrs.get(
            "appointment",
            self.instance.appointment if self.instance else None,
        )

        queryset = Billing.objects.filter(
            appointment=appointment,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "appointment": "Bill already exists for this appointment."
                }
            )

        return attrs

    def create(self, validated_data):

        appointment = validated_data["appointment"]

        consultation_fee = appointment.doctor.consultation_fee

        medicine_charges = validated_data.get(
            "medicine_charges",
            Decimal("0.00"),
        )

        test_charges = validated_data.get(
            "test_charges",
            Decimal("0.00"),
        )

        discount = validated_data.get(
            "discount",
            Decimal("0.00"),
        )

        total_amount = (
            consultation_fee
            + medicine_charges
            + test_charges
            - discount
        )

        bill = Billing.objects.create(
            appointment=appointment,
            consultation_fee=consultation_fee,
            medicine_charges=medicine_charges,
            test_charges=test_charges,
            discount=discount,
            total_amount=total_amount,
        )

        return bill

    def update(self, instance, validated_data):

        instance.appointment = validated_data.get(
            "appointment",
            instance.appointment,
        )

        instance.medicine_charges = validated_data.get(
            "medicine_charges",
            instance.medicine_charges,
        )

        instance.test_charges = validated_data.get(
            "test_charges",
            instance.test_charges,
        )

        instance.discount = validated_data.get(
            "discount",
            instance.discount,
        )

        instance.payment_status = validated_data.get(
            "payment_status",
            instance.payment_status,
        )

        instance.consultation_fee = (
            instance.appointment.doctor.consultation_fee
        )

        instance.total_amount = (
            instance.consultation_fee
            + instance.medicine_charges
            + instance.test_charges
            - instance.discount
        )

        instance.save()

        return instance