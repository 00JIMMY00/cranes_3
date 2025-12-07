from rest_framework import serializers
from .models import Driver, Loan


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'base_salary', 'current_balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'current_balance', 'created_at', 'updated_at']


class LoanSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.name', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'driver', 'driver_name', 'amount', 'date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
