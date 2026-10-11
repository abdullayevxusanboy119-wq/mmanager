from django.db import models
from django.conf import settings
from customers.models import Customer
from products.models import Product


class Sale(models.Model):
    TYPE_CHOICES = (
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('credit', 'Kredit'),
        ('transfer', "O'tkazma"),
    )
    STATUS_CHOICES = (
        ('paid', "To'langan"),
        ('partial', 'Qisman'),
    )

    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, related_name='sales', on_delete=models.SET_NULL, null=True, blank=True
    )
    customer_name = models.CharField(max_length=255, blank=True)  # mijoz o'chirilsa ham chek uchun saqlab qolinadi
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='cash')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    sold_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Sale #{self.id} - {self.customer_name or 'Nomalum'}"

    class Meta:
        ordering = ['-date']


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)  # mahsulot nomi (tarixiy nusxa)
    model = models.CharField(max_length=100, blank=True, null=True)
    selling = models.DecimalField(max_digits=14, decimal_places=2)
    purchase = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    qty = models.PositiveIntegerField(default=1)

    @property
    def item_profit(self):
        return (self.selling - self.purchase) * self.qty

    def __str__(self):
        return f"{self.name} x{self.qty}"