from django.db import models
from customers.models import Customer


class Repair(models.Model):
    STATUS_CHOICES = (
        ('received', 'Qabul qilindi'),
        ('repairing', "Ta'mirlanmoqda"),
        ('ready', 'Tayyor'),
    )

    customer = models.ForeignKey(
        Customer, related_name='repairs', on_delete=models.SET_NULL, null=True, blank=True
    )
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    issue = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='received')
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # keyingi statusga o'tkazish uchun tartib (frontend'dagi updateRepairStatus() mantig'i)
    STATUS_ORDER = ['received', 'repairing', 'ready']

    def advance_status(self):
        idx = self.STATUS_ORDER.index(self.status)
        next_idx = (idx + 1) % len(self.STATUS_ORDER)
        self.status = self.STATUS_ORDER[next_idx]

    def __str__(self):
        return f"{self.customer_name} - {self.model} ({self.status})"

    class Meta:
        ordering = ['-created_at']