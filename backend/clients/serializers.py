from rest_framework import serializers
from .models import Client, Payment


class PaymentSerializer(serializers.ModelSerializer):
    method_display = serializers.CharField(source='get_method_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'client', 'amount', 'date', 'method', 'method_display', 
                  'reference', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClientSerializer(serializers.ModelSerializer):
    services_count = serializers.IntegerField(read_only=True)
    active_rentals_count = serializers.IntegerField(read_only=True)
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    outstanding_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'address', 'phone', 'email', 
                  'services_count', 'active_rentals_count', 
                  'total_revenue', 'total_paid', 'outstanding_balance',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 
                           'services_count', 'active_rentals_count',
                           'total_revenue', 'total_paid', 'outstanding_balance']
