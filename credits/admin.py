from django.contrib import admin
from .models import Credit


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ['debtor_name', 'car_number', 'debtor_phone', 'price', 'initial_payment', 'credit_term', 'fuel_type',
                    'is_closed', 'closed_at', 'created_at']
    list_filter = ['fuel_type', 'is_closed']
    search_fields = ['debtor_name', 'car_number']
