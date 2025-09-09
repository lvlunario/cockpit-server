from django.contrib import admin
from .models import Cashier, Event, Bet

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('event', 'bet_choice', 'amount', 'cashier', 'timestamp')
    list_filter = ('event', 'cashier')
    search_fields = ('bet_choice',)
    
    def formatted_amount(self, obj):
        # Check if the amount is a whole number
        if obj.amount == obj.amount.to_integral_value():
            # If so, display as an integer with a comma separator (e.g., ₱10,000)
            return f"₱{int(obj.amount):,}"
        else: 
            # If it has centavos, display with two decimal places (e.g., ₱10,500.50)
            return f"₱{obj.amount:,.2f}"
        
    # Set the column header text in the admin
    formatted_amount.short_description = 'Amount'
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'is_active')
    
@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    list_display = ('name', 'station_id')