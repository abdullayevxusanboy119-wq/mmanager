from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    profit = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'model', 'imei', 'category',
            'purchase', 'selling', 'qty', 'min_qty',
            'profit', 'archived', 'created_at', 'updated_at',
        ]

    def validate_imei(self, value):
        if not value:
            return value
        qs = Product.objects.filter(imei__iexact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Bu IMEI raqami allaqachon mavjud.")
        return value