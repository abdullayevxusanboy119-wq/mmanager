from rest_framework import serializers
from django.db import transaction
from .models import Sale, SaleItem
from products.models import Product


class SaleItemInputSerializer(serializers.Serializer):
    """POST qilinganda cart'dan keladigan item shakli."""
    id = serializers.IntegerField()  # product id
    qty = serializers.IntegerField(min_value=1)


class SaleItemSerializer(serializers.ModelSerializer):
    item_profit = serializers.ReadOnlyField()

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'name', 'model', 'selling', 'purchase', 'qty', 'item_profit']


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    # yozishda faqat product id + qty ro'yxati yuboriladi
    cart_items = SaleItemInputSerializer(many=True, write_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'date', 'customer', 'customer_name', 'total', 'profit',
            'type', 'status', 'items', 'cart_items',
        ]
        read_only_fields = ['total', 'profit']

    def validate_cart_items(self, value):
        if not value:
            raise serializers.ValidationError("Savat bo'sh bo'lishi mumkin emas.")
        return value

    def create(self, validated_data):
        cart_items = validated_data.pop('cart_items')
        request = self.context.get('request')

        with transaction.atomic():
            # avval barcha mahsulotlarni tekshiramiz (qoldiq yetarli bo'lishi kerak)
            products_map = {}
            for entry in cart_items:
                try:
                    product = Product.objects.select_for_update().get(id=entry['id'])
                except Product.DoesNotExist:
                    raise serializers.ValidationError(f"Mahsulot topilmadi: id={entry['id']}")
                if product.qty < entry['qty']:
                    raise serializers.ValidationError(
                        f"'{product.name}' uchun qoldiq yetarli emas (mavjud: {product.qty}, so'ralgan: {entry['qty']})"
                    )
                products_map[entry['id']] = product

            total = 0
            profit = 0
            sale = Sale.objects.create(
                customer=validated_data.get('customer'),
                customer_name=validated_data.get('customer_name', ''),
                type=validated_data.get('type', 'cash'),
                status=validated_data.get('status', 'paid'),
                sold_by=request.user if request else None,
                total=0,
                profit=0,
            )

            for entry in cart_items:
                product = products_map[entry['id']]
                qty = entry['qty']

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    name=product.name,
                    model=product.model,
                    selling=product.selling,
                    purchase=product.purchase,
                    qty=qty,
                )

                product.qty -= qty
                product.save()

                total += product.selling * qty
                profit += (product.selling - product.purchase) * qty

            sale.total = total
            sale.profit = profit
            sale.save()

        return sale