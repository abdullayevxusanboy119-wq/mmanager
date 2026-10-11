from rest_framework import serializers
from .models import Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = [
            'id', 'customer', 'customer_name', 'phone', 'total', 'paid',
            'remaining', 'months', 'monthly', 'due_date', 'status', 'created_at',
        ]
        read_only_fields = ['remaining', 'status']

    def validate(self, attrs):
        total = attrs.get('total', getattr(self.instance, 'total', 0))
        paid = attrs.get('paid', getattr(self.instance, 'paid', 0))
        if paid > total:
            raise serializers.ValidationError(
                "To'langan summa umumiy summadan katta bo'lishi mumkin emas."
            )
        return attrs

    def create(self, validated_data):
        total = validated_data['total']
        paid = validated_data.get('paid', 0)
        validated_data['remaining'] = total - paid
        credit = Credit(**validated_data)
        credit.refresh_status()
        credit.save()
        return credit


class CreditPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0.01)

    def validate_amount(self, value):
        credit = self.context['credit']
        if value > credit.remaining:
            raise serializers.ValidationError("To'lov qoldiqdan ko'p bo'lishi mumkin emas.")
        return value