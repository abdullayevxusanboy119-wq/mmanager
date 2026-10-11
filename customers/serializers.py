from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    purchases = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()
    last_purchase = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'email', 'address',
            'purchases', 'total_spent', 'last_purchase',
            'created_at', 'updated_at',
        ]

    def get_purchases(self, obj):
        # 'sales' app hali ulanmagan bo'lsa xato bermasligi uchun himoyalangan
        try:
            return obj.purchases
        except Exception:
            return 0

    def get_total_spent(self, obj):
        try:
            return obj.total_spent
        except Exception:
            return 0

    def get_last_purchase(self, obj):
        try:
            return obj.last_purchase
        except Exception:
            return None