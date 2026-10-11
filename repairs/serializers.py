from rest_framework import serializers
from .models import Repair


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = [
            'id', 'customer', 'customer_name', 'phone', 'model', 'issue',
            'status', 'price', 'notified', 'created_at', 'updated_at',
        ]