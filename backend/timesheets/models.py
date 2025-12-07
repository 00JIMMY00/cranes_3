from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from drivers.models import Driver
from cranes.models import Crane
from clients.models import Client


class TimeSheet(models.Model):
    SHIFT_CHOICES = [
        ('8h', '8 Hours'),
        ('9h', '9 Hours'),
        ('12h', '12 Hours'),
    ]
    
    # Core fields
    date = models.DateField()
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='timesheets')
    crane = models.ForeignKey(Crane, on_delete=models.PROTECT, related_name='timesheets')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='timesheets')
    
    # Time fields
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Calculated fields
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    shift_type = models.CharField(max_length=3, choices=SHIFT_CHOICES, default='8h')
    
    # Financial fields (calculated on save)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    driver_wage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # For sub-rented cranes
    
    # Metadata
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Time Sheet'
        verbose_name_plural = 'Time Sheets'
    
    def __str__(self):
        return f"{self.date} - {self.driver.name} - {self.crane.name}"
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError('End time must be after start time')
    
    def calculate_hours(self):
        """Calculate total hours and overtime from start/end times."""
        if not self.start_time or not self.end_time:
            return
        
        from datetime import datetime, timedelta
        
        # Convert times to datetime for calculation
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        
        # Handle overnight shifts
        if end <= start:
            end += timedelta(days=1)
        
        diff = end - start
        self.total_hours = Decimal(str(diff.total_seconds() / 3600))
        
        # Determine shift type and overtime
        if self.total_hours <= 8:
            self.shift_type = '8h'
            self.overtime_hours = Decimal('0')
        elif self.total_hours <= 9:
            self.shift_type = '9h'
            self.overtime_hours = self.total_hours - Decimal('8')
        else:
            self.shift_type = '12h'
            self.overtime_hours = self.total_hours - Decimal('8')
    
    def calculate_financials(self):
        """Calculate revenue, driver wage, and commission based on shift type."""
        if not self.crane:
            return
        
        # Get rate based on shift type
        if self.shift_type == '8h':
            self.revenue = self.crane.rate_8h
        elif self.shift_type == '9h':
            self.revenue = self.crane.rate_9h
        else:  # 12h
            self.revenue = self.crane.rate_12h
        
        # Calculate driver wage (base salary per day + overtime bonus)
        if self.driver:
            # Assuming base_salary is monthly, calculate daily rate (30 days)
            daily_rate = self.driver.base_salary / Decimal('30')
            overtime_rate = daily_rate / Decimal('8') * Decimal('1.5')  # 1.5x for overtime
            self.driver_wage = daily_rate + (self.overtime_hours * overtime_rate)
        
        # Calculate commission for sub-rented cranes
        if self.crane.is_subrented:
            self.commission = self.revenue - self.crane.owner_cost
        else:
            self.commission = self.revenue  # Full revenue if owned
    
    def save(self, *args, **kwargs):
        self.calculate_hours()
        self.calculate_financials()
        super().save(*args, **kwargs)


class MonthlyTimeSheet(models.Model):
    """
    Monthly time sheet header - matches hard copy format.
    Contains header info and links to 31 daily entries.
    """
    # Header fields (matching hard copy)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='monthly_sheets',
                               verbose_name='Project/Customer')
    crane = models.ForeignKey(Crane, on_delete=models.PROTECT, related_name='monthly_sheets',
                              verbose_name='Machine/Equipment')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='monthly_sheets',
                               verbose_name='Operator')
    location = models.CharField(max_length=255, blank=True, default='', verbose_name='Location/Site')
    
    # Month/Year
    month = models.PositiveIntegerField()  # 1-12
    year = models.PositiveIntegerField()
    
    # Calculated totals
    total_operating_hours = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_attendance_hours = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_trips = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_driver_wage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Supervisor
    supervisor_name = models.CharField(max_length=255, blank=True, default='')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['client', 'crane', 'driver', 'month', 'year']
        verbose_name = 'Monthly Time Sheet'
        verbose_name_plural = 'Monthly Time Sheets'
    
    def __str__(self):
        return f"{self.get_month_display()} {self.year} - {self.driver.name} - {self.crane.name}"
    
    def get_month_display(self):
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        return months[self.month] if 1 <= self.month <= 12 else str(self.month)
    
    def get_month_display_ar(self):
        months_ar = ['', 'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                     'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
        return months_ar[self.month] if 1 <= self.month <= 12 else str(self.month)
    
    def calculate_totals(self):
        """Calculate monthly totals from daily entries."""
        from django.db.models import Sum
        
        totals = self.daily_entries.aggregate(
            operating=Sum('operating_hours'),
            attendance=Sum('attendance_hours'),
            trips=Sum('trips')
        )
        
        self.total_operating_hours = totals['operating'] or Decimal('0')
        self.total_attendance_hours = totals['attendance'] or Decimal('0')
        self.total_trips = totals['trips'] or 0
        
        # Calculate revenue based on operating hours
        # Using crane rates based on daily shift patterns
        total_revenue = Decimal('0')
        total_wage = Decimal('0')
        
        for entry in self.daily_entries.filter(operating_hours__gt=0):
            hours = entry.operating_hours
            if hours <= 8:
                total_revenue += self.crane.rate_8h
            elif hours <= 9:
                total_revenue += self.crane.rate_9h
            else:
                total_revenue += self.crane.rate_12h
            
            # Driver wage calculation
            daily_rate = self.driver.base_salary / Decimal('30')
            overtime = max(Decimal('0'), hours - Decimal('8'))
            overtime_rate = daily_rate / Decimal('8') * Decimal('1.5')
            total_wage += daily_rate + (overtime * overtime_rate)
        
        self.total_revenue = total_revenue
        self.total_driver_wage = total_wage
    
    def create_daily_entries(self):
        """Create 31 daily entry rows for this sheet."""
        import calendar
        from datetime import date
        
        # Get number of days in this month
        days_in_month = calendar.monthrange(self.year, self.month)[1]
        
        for day in range(1, 32):
            if day <= days_in_month:
                entry_date = date(self.year, self.month, day)
                weekday = entry_date.strftime('%A')
                weekday_ar = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 
                              'الجمعة', 'السبت', 'الأحد'][entry_date.weekday()]
            else:
                entry_date = None
                weekday = ''
                weekday_ar = ''
            
            DailyEntry.objects.create(
                monthly_sheet=self,
                day_number=day,
                date=entry_date,
                weekday=weekday,
                weekday_ar=weekday_ar
            )
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.create_daily_entries()


class DailyEntry(models.Model):
    """
    Single day entry in a monthly time sheet.
    Matches hard copy columns: م, اليوم, التاريخ, من, إلى, ساعات التشغيل, رحلات, البيان, ساعات الحضور
    """
    monthly_sheet = models.ForeignKey(MonthlyTimeSheet, on_delete=models.CASCADE, related_name='daily_entries')
    
    # Row info (auto-generated)
    day_number = models.PositiveIntegerField()  # م (1-31)
    date = models.DateField(null=True, blank=True)  # التاريخ
    weekday = models.CharField(max_length=20, blank=True)  # اليوم (English)
    weekday_ar = models.CharField(max_length=20, blank=True)  # اليوم (Arabic)
    
    # Time inputs (Changed to Decimal for simple hour entry)
    from_time = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='From (من)')
    from_period = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')], default='AM', verbose_name='AM/PM')
    
    to_time = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='To (إلى)')
    to_period = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')], default='PM', verbose_name='AM/PM')
    
    # Calculated/Input fields
    operating_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                          verbose_name='Operating Hours (إجمالي ساعات التشغيل)')
    trips = models.PositiveIntegerField(default=0, verbose_name='Trips (رحلات)')
    notes = models.TextField(blank=True, default='', verbose_name='Notes (البيان)')
    attendance_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                           verbose_name='Attendance Hours (إجمالي ساعات الحضور)')
    
    class Meta:
        ordering = ['monthly_sheet', 'day_number']
        unique_together = ['monthly_sheet', 'day_number']
        verbose_name = 'Daily Entry'
        verbose_name_plural = 'Daily Entries'
    
    def __str__(self):
        return f"Day {self.day_number} - {self.date}"
    
    def calculate_operating_hours(self):
        """Calculate operating hours from from_time and to_time (decimal hours) with AM/PM."""
        if self.from_time is None or self.to_time is None:
            self.operating_hours = Decimal('0')
            return
        
        # Ensure values are Decimal (handles potential string input from forms)
        try:
            start_val = Decimal(str(self.from_time))
            end_val = Decimal(str(self.to_time))
        except:
            self.operating_hours = Decimal('0')
            return

        # Convert start time to 24h
        if self.from_period == 'PM' and start_val < 12:
            start_val += 12
        elif self.from_period == 'AM' and start_val == 12:
            start_val = Decimal('0')
            
        # Convert end time to 24h
        if self.to_period == 'PM' and end_val < 12:
            end_val += 12
        elif self.to_period == 'AM' and end_val == 12:
            end_val = Decimal('0')
            
        # Calculate difference
        diff = end_val - start_val
        
        # Handle overnight (e.g. 8 PM to 2 AM -> 20 to 2 -> -18 -> +24 = 6)
        if diff < 0:
            diff += Decimal('24')
            
        self.operating_hours = diff
    
    def save(self, *args, **kwargs):
        self.calculate_operating_hours()
        super().save(*args, **kwargs)
        
        # Update monthly totals
        if self.monthly_sheet_id:
            self.monthly_sheet.calculate_totals()
            MonthlyTimeSheet.objects.filter(pk=self.monthly_sheet_id).update(
                total_operating_hours=self.monthly_sheet.total_operating_hours,
                total_attendance_hours=self.monthly_sheet.total_attendance_hours,
                total_trips=self.monthly_sheet.total_trips,
                total_revenue=self.monthly_sheet.total_revenue,
                total_driver_wage=self.monthly_sheet.total_driver_wage
            )
