from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import date
from .models import Client, Payment
from timesheets.models import MonthlyTimeSheet
from drivers.models import Driver
from cranes.models import Crane


class ClientStatsTestCase(TestCase):
    """Test cases for Client financial stats and payment tracking."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client.objects.create(
            name="Acme Corp",
            phone="123-456-7890",
            email="acme@example.com"
        )
        self.driver = Driver.objects.create(
            name="Test Driver",
            base_salary=Decimal('3000')
        )
        self.crane = Crane.objects.create(
            name="Test Crane"
        )
    
    def test_client_initial_balance_is_zero(self):
        """Test that a new client has zero balance."""
        self.assertEqual(self.client.outstanding_balance, Decimal('0'))
        self.assertEqual(self.client.total_revenue, Decimal('0'))
        self.assertEqual(self.client.total_paid, Decimal('0'))
    
    def test_client_services_count_initial(self):
        """Test that a new client has zero services."""
        self.assertEqual(self.client.services_count, 0)
    
    def test_client_active_rentals_count_initial(self):
        """Test that a new client has zero active rentals."""
        self.assertEqual(self.client.active_rentals_count, 0)
    
    def test_payment_creation(self):
        """Test creating a payment."""
        payment = Payment.objects.create(
            client=self.client,
            amount=Decimal('1000'),
            date=date.today(),
            method='CASH',
            reference='',
            notes='Test payment'
        )
        self.assertEqual(payment.amount, Decimal('1000'))
        self.assertEqual(payment.method, 'CASH')
        self.assertEqual(self.client.total_paid, Decimal('1000'))
    
    def test_balance_after_timesheet_and_payment(self):
        """Test balance updates after adding timesheet and payment."""
        # Create a timesheet with revenue
        today = timezone.now().date()
        sheet = MonthlyTimeSheet.objects.create(
            client=self.client,
            driver=self.driver,
            crane=self.crane,
            month=today.month,
            year=today.year,
            start_date=today,
            end_date=today,
        )
        
        # Update total_revenue directly (bypassing save recalculation)
        # This simulates a timesheet with calculated revenue
        MonthlyTimeSheet.objects.filter(pk=sheet.pk).update(total_revenue=Decimal('5000'))
        
        # Check that balance increased
        self.assertEqual(self.client.total_revenue, Decimal('5000'))
        self.assertEqual(self.client.outstanding_balance, Decimal('5000'))
        
        # Add a partial payment
        Payment.objects.create(
            client=self.client,
            amount=Decimal('2000'),
            date=date.today(),
            method='BANK_TRANSFER'
        )
        
        self.assertEqual(self.client.total_paid, Decimal('2000'))
        self.assertEqual(self.client.outstanding_balance, Decimal('3000'))
    
    def test_active_rentals_count(self):
        """Test active rentals count updates when timesheet is added for current month."""
        today = timezone.now().date()
        
        # Create a timesheet for current month
        MonthlyTimeSheet.objects.create(
            client=self.client,
            driver=self.driver,
            crane=self.crane,
            month=today.month,
            year=today.year,
            start_date=today,
            end_date=today,
        )
        
        self.client.refresh_from_db()
        self.assertEqual(self.client.active_rentals_count, 1)
        self.assertEqual(self.client.services_count, 1)
    
    def test_payment_methods(self):
        """Test all payment methods are valid."""
        methods = ['CASH', 'BANK_TRANSFER', 'CHEQUE']
        
        for idx, method in enumerate(methods):
            payment = Payment.objects.create(
                client=self.client,
                amount=Decimal('100'),
                date=date.today(),
                method=method
            )
            self.assertEqual(payment.method, method)
