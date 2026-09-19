from rest_framework import serializers
from .models import Payment
from django.utils import timezone
from django.db import transaction
import calendar


class PaymentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source="member.name",
        read_only=True
    )







    class Meta:
        model = Payment
        fields = [
            'id',
            "name",
            "amount",
            "status",
            'payment_method',
            "payment_date",
            'created_at'
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source="member.name",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "status",
            "payment_date",
            "amount",
        ]

    def validate(self, attrs):
        payment_method = attrs.get("payment_method")

        if not payment_method:
            raise serializers.ValidationError({
                "payment_method": "Payment method is required."
            })

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        # Get member
        member = validated_data["member"]

        # Amount comes from member's monthly fee
        validated_data["amount"] = member.monthly_fee

        # Automatically mark payment as PAID
        validated_data["status"] = "PAID"

        # Payment date = today
        payment_date = timezone.localdate()
        validated_data["payment_date"] = payment_date

        # Create payment
        payment = Payment.objects.create(
            **validated_data
        )

        # Calculate next due date
        if member.payment_due_date is None:
            # If there is no existing due date,
            # next payment is one month from today.
            member.payment_due_date = add_one_month(
                payment_date
            )
        else:
            # Normally move the existing due date
            # forward by one calendar month.
            member.payment_due_date = add_one_month(
                member.payment_due_date
            )

        # Save updated due date
        member.save(
            update_fields=["payment_due_date"]
        )

        return payment


def add_one_month(date):

    year = date.year
    month = date.month + 1

    if month > 12:
        month = 1
        year += 1

    # Number of days in the target month
    last_day = calendar.monthrange(
        year,
        month
    )[1]

    # Keep the same day when possible.
    # Example: 18 -> 18
    # Example: 31 -> 30/29/28 when necessary.
    day = min(
        date.day,
        last_day
    )

    return date.replace(
        year=year,
        month=month,
        day=day
    )