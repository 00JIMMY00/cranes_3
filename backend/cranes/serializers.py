from rest_framework import serializers
from .models import Crane


class CraneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crane
        fields = ['id', 'name', 'rate_8h', 'rate_9h', 'rate_12h', 'is_subrented', 'owner_cost', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
