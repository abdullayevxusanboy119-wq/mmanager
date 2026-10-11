from django.db import models
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer


def default_due_date():
    return timezone.now().date() + timedelta(days=30)


class Credit(models.Model):
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('completed', "To'langan"),
        ('overdue', "Muddati o'tgan"),
    )

    customer = models.ForeignKey(
        Customer, related_name='credits', on_delete=models.SET_NULL, null=True, blank=True
    )
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    remaining = models.DecimalField(max_digits=14, decimal_places=2)
    months = models.PositiveIntegerField(default=1)
    monthly = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    due_date = models.DateField(default=default_due_date)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def refresh_status(self):
        """updateCreditStatuses() frontend mantiqiga mos: remaining/due_date asosida statusni yangilaydi."""
        if self.remaining <= 0:
            self.status = 'completed'
        elif self.due_date < timezone.now().date():
            self.status = 'overdue'
        else:
            self.status = 'active'

    def __str__(self):
        return f"{self.customer_name} - {self.remaining}"

    class Meta:
        ordering = ['-created_at']