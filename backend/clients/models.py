from django.db import models
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal


class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @property
    def services_count(self):
        """Total number of timesheets (services) for this client."""
        return self.monthly_sheets.count()

    @property
    def active_rentals_count(self):
        """Number of active rentals (timesheets with end_date >= today or in current month)."""
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        # Count sheets where end_date is in the future OR current month/year matches
        return self.monthly_sheets.filter(
            models.Q(end_date__gte=today) |
            models.Q(month=current_month, year=current_year)
        ).distinct().count()

    @property
    def total_revenue(self):
        """Sum of total_revenue from all timesheets."""
        result = self.monthly_sheets.aggregate(total=Sum('total_revenue'))
        return result['total'] or Decimal('0')

    @property
    def total_paid(self):
        """Sum of all payments made by this client."""
        result = self.payments.aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0')

    @property
    def outstanding_balance(self):
        """Outstanding balance = total revenue - total paid."""
        return self.total_revenue - self.total_paid


class Payment(models.Model):
    """Represents a payment made by a client."""
    
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    reference = models.CharField(max_length=255, blank=True, default='',
                                 help_text='Cheque number or bank transaction ID')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.name} - {self.amount} ({self.get_method_display()}) on {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
