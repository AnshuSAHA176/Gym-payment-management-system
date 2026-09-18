from rest_framework import serializers
from .models import Member



class MemberSerializer(serializers.ModelSerializer):
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