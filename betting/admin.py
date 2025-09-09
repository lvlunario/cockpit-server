from django.contrib import admin
from .models import Cashier, Event, Bet

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('event', 'bet_choice', 'amount', 'cashier', 'timestamp')
    list_filter = ('event', 'cashier')
    search_fields = ('bet_choice',)
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'is_active')
    
@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    list_display = ('name', 'station_id')