from django.contrib import admin
from .models import Client, Payment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['client', 'amount', 'date', 'method', 'reference', 'created_at']
    list_filter = ['method', 'date']
    search_fields = ['client__name', 'reference', 'notes']
    date_hierarchy = 'date'
