from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal


class Driver(models.Model):
    name = models.CharField(max_length=255)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    
    def recalculate_balance(self):
        """Recalculate balance from wages earned minus loans taken."""
        from timesheets.models import TimeSheet
        
        # Total wages earned from timesheets
        total_wages = TimeSheet.objects.filter(driver=self).aggregate(
            total=models.Sum('driver_wage')
        )['total'] or Decimal('0')
        
        # Total loans taken
        total_loans = self.loans.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0')
        
        self.current_balance = total_wages - total_loans
        self.save(update_fields=['current_balance'])


class Loan(models.Model):
    """Record of cash loans given to drivers."""
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"{self.driver.name} - {self.amount} EGP ({self.date})"


# Signals to update driver balance when loans change
@receiver(post_save, sender=Loan)
def update_driver_balance_on_loan_save(sender, instance, **kwargs):
    instance.driver.recalculate_balance()


@receiver(post_delete, sender=Loan)
def update_driver_balance_on_loan_delete(sender, instance, **kwargs):
    instance.driver.recalculate_balance()
