from rest_framework import serializers
from .models import Payment
from django.utils import timezone
from members.models  import Member
from datetime import timedelta
from django.db import transaction

import calendar



class PaymentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='member.name',read_only=True)
    class Meta:
        model = Payment
        fields =[
            'name',
            'amount',
            'status',
            'payment_date'
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

        # Get the member from the incoming data
        member = validated_data["member"]

        # Amount comes from the member's monthly fee
        validated_data["amount"] = member.monthly_fee

        # Payment is automatically marked as PAID
        validated_data["status"] = "PAID"

        # Payment date is automatically today's date
        payment_date = timezone.localdate()
        validated_data["payment_date"] = payment_date

        # Create payment
        payment = Payment.objects.create(**validated_data)

        # Calculate next due date
        if member.payment_due_date == None:
            member.payment_due_date = add_one_month(member.payment_due_datepayment_due_date)

        member.payment_due_date = add_one_month(member.payment_due_datepayment_due_date)
            

        # Save updated due date
        member.save(update_fields=["payment_due_date"])

        return payment









def add_one_month(date):


    year = date.year
    month = date.month + 1

    if month > 12:
        month = 1
        year += 1

    last_day = calendar.monthrange(year, month)[1]

    day = min(date.day, last_day)

    return date.replace(
        year=year,
        month=month,
        day=day,
    )
