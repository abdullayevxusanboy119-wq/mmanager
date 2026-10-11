from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('telefon', 'Telefon'),
        ('aksesuar', 'Aksesuar'),
    )

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=100, blank=True, null=True)
    imei = models.CharField(max_length=50, blank=True, null=True, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='telefon')
    purchase = models.DecimalField(max_digits=14, decimal_places=2)
    selling = models.DecimalField(max_digits=14, decimal_places=2)
    qty = models.PositiveIntegerField(default=0)
    min_qty = models.PositiveIntegerField(default=3)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def profit(self):
        return self.selling - self.purchase

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        ordering = ['-created_at']