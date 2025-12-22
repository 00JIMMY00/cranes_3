from rest_framework import serializers
from .models import Crane
from timesheets.models import MonthlyTimeSheet


class CraneAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for crane assignment history."""
    client_name = serializers.CharField(source='client.name', read_only=True)
    driver_name = serializers.CharField(source='driver.name', read_only=True)
    
    class Meta:
        model = MonthlyTimeSheet
        fields = ['id', 'client_name', 'driver_name', 'location', 'start_date', 'end_date']


class CraneSerializer(serializers.ModelSerializer):
    assignments = CraneAssignmentSerializer(source='monthly_sheets', many=True, read_only=True)
    
    class Meta:
        model = Crane
        fields = ['id', 'name', 'is_subrented', 'owner_cost', 'created_at', 'updated_at', 'assignments']
        read_only_fields = ['id', 'created_at', 'updated_at', 'assignments']

