from django.contrib import admin
from .models import Driver, Loan


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_salary', 'current_balance', 'created_at']
    search_fields = ['name']
    readonly_fields = ['current_balance', 'created_at', 'updated_at']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['driver', 'amount', 'date', 'created_at']
    list_filter = ['driver', 'date']
    search_fields = ['driver__name', 'notes']
    date_hierarchy = 'date'
