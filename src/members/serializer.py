from rest_framework import serializers
from .models import Member
from payment.serializer import PaymentSerializer


class MemberSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True,read_only=True)
    class Meta:
        model= Member

        fields = '__all__'



class MemberDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields=[
            'name',
            'phone',
            'payment_due_date',
            'is_active'
        ]
class OverDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields=[
            'member_id',
            'name',
            'phone',
            'payment_due_date',
            'is_active'
        ]