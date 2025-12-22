from django.test import TestCase
from timesheets.models import MonthlyTimeSheet, DailyEntry
from clients.models import Client
from cranes.models import Crane
from drivers.models import Driver
from decimal import Decimal
from datetime import date

class HourlyRateTests(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Test Client")
        self.crane = Crane.objects.create(name="Test Crane")
        self.driver = Driver.objects.create(name="Test Driver")

    def test_hourly_rate_fields(self):
        # Test price_per_day on MonthlyTimeSheet with date range
        sheet = MonthlyTimeSheet.objects.create(
            client=self.client,
            crane=self.crane,
            driver=self.driver,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 5),
            price_per_day=150
        )
        self.assertEqual(sheet.price_per_day, 150)
        
        # Test hourly_rate on DailyEntry (should be integer)
        entry = sheet.daily_entries.first()
        self.assertTrue(hasattr(entry, 'hourly_rate'), "hourly_rate field does not exist on DailyEntry")
        
        # Manually set hourly_rate to verify field behavior
        entry.hourly_rate = 200
        entry.save()
        entry.refresh_from_db()
        self.assertEqual(entry.hourly_rate, 200)

    def test_daily_total_calculation(self):
        # Test daily_total = operating_hours * hourly_rate
        sheet = MonthlyTimeSheet.objects.create(
            client=self.client,
            crane=self.crane,
            driver=self.driver,
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 3),
            price_per_day=50
        )
        
        entry = sheet.daily_entries.first()
        entry.from_time = 8
        entry.from_period = 'AM'
        entry.to_time = 4
        entry.to_period = 'PM'
        entry.hourly_rate = 100
        entry.save()
        
        entry.refresh_from_db()
        # 8 AM to 4 PM = 8 hours, 8 * 100 = 800
        self.assertEqual(entry.operating_hours, 8)
        self.assertEqual(entry.daily_total, 800)


class CraneOverlapValidationTests(TestCase):
    """Tests for preventing overlapping crane assignments."""
    
    def setUp(self):
        self.client1 = Client.objects.create(name="Client A")
        self.client2 = Client.objects.create(name="Client B")
        self.crane = Crane.objects.create(name="Crane 1")
        self.crane2 = Crane.objects.create(name="Crane 2")
        self.driver = Driver.objects.create(name="Driver A")
        
        # Create an existing assignment: Jan 1 - Jan 15
        self.existing_sheet = MonthlyTimeSheet.objects.create(
            client=self.client1,
            crane=self.crane,
            driver=self.driver,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 15),
            location="Site A"
        )
    
    def test_exact_overlap_blocked(self):
        """Test that exact date range overlap is blocked."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError) as context:
            MonthlyTimeSheet.objects.create(
                client=self.client2,
                crane=self.crane,
                driver=self.driver,
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 15),
                location="Site B"
            )
        self.assertIn('crane', str(context.exception))
    
    def test_partial_overlap_at_end_blocked(self):
        """Test that partial overlap at the end is blocked."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            MonthlyTimeSheet.objects.create(
                client=self.client2,
                crane=self.crane,
                driver=self.driver,
                start_date=date(2024, 1, 10),  # Overlaps from Jan 10-15
                end_date=date(2024, 1, 20),
                location="Site B"
            )
    
    def test_partial_overlap_at_start_blocked(self):
        """Test that partial overlap at the start is blocked."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            MonthlyTimeSheet.objects.create(
                client=self.client2,
                crane=self.crane,
                driver=self.driver,
                start_date=date(2023, 12, 25),  # Overlaps from Jan 1-5
                end_date=date(2024, 1, 5),
                location="Site B"
            )
    
    def test_enclosing_range_blocked(self):
        """Test that a range completely enclosing an existing assignment is blocked."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            MonthlyTimeSheet.objects.create(
                client=self.client2,
                crane=self.crane,
                driver=self.driver,
                start_date=date(2023, 12, 1),  # Completely encloses Jan 1-15
                end_date=date(2024, 2, 1),
                location="Site B"
            )
    
    def test_inside_range_blocked(self):
        """Test that a range completely inside an existing assignment is blocked."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            MonthlyTimeSheet.objects.create(
                client=self.client2,
                crane=self.crane,
                driver=self.driver,
                start_date=date(2024, 1, 5),  # Inside Jan 1-15
                end_date=date(2024, 1, 10),
                location="Site B"
            )
    
    def test_sequential_after_allowed(self):
        """Test that sequential assignment after existing is allowed."""
        sheet = MonthlyTimeSheet.objects.create(
            client=self.client2,
            crane=self.crane,
            driver=self.driver,
            start_date=date(2024, 1, 16),  # Day after existing ends
            end_date=date(2024, 1, 31),
            location="Site B"
        )
        self.assertIsNotNone(sheet.pk)
    
    def test_sequential_before_allowed(self):
        """Test that sequential assignment before existing is allowed."""
        sheet = MonthlyTimeSheet.objects.create(
            client=self.client2,
            crane=self.crane,
            driver=self.driver,
            start_date=date(2023, 12, 15),  # Before existing starts
            end_date=date(2023, 12, 31),
            location="Site B"
        )
        self.assertIsNotNone(sheet.pk)
    
    def test_update_self_allowed(self):
        """Test that updating an existing sheet doesn't trigger self-conflict."""
        self.existing_sheet.location = "Site A Updated"
        self.existing_sheet.save()  # Should not raise
        self.existing_sheet.refresh_from_db()
        self.assertEqual(self.existing_sheet.location, "Site A Updated")
    
    def test_different_crane_allowed(self):
        """Test that overlapping dates are allowed for different cranes."""
        sheet = MonthlyTimeSheet.objects.create(
            client=self.client2,
            crane=self.crane2,  # Different crane
            driver=self.driver,
            start_date=date(2024, 1, 1),  # Same dates as existing
            end_date=date(2024, 1, 15),
            location="Site B"
        )
        self.assertIsNotNone(sheet.pk)
    
    def test_end_date_before_start_date_invalid(self):
        """Test that end_date before start_date raises validation error."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError) as context:
            MonthlyTimeSheet.objects.create(
                client=self.client2,
                crane=self.crane2,
                driver=self.driver,
                start_date=date(2024, 2, 15),
                end_date=date(2024, 2, 1),  # Before start_date
                location="Site B"
            )
        self.assertIn('end_date', str(context.exception))

