from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def purchases(self):
        return self.sales.count()

    @property
    def total_spent(self):
        return sum(sale.total for sale in self.sales.all())

    @property
    def last_purchase(self):
        last = self.sales.order_by('-date').first()
        return last.date if last else None

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        ordering = ['-created_at']