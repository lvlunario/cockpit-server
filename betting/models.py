from django.db import models
import uuid

class Cashier(models.Model):
    station_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name} ({self.station_id})"
    
class Event(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField()
    
    WINNER_CHOICES = [
        ('MERON', 'Meron'),
        ('WALA', 'Wala'),
        ('DRAW', 'Draw'),
    ]
    outcome = models.CharField(max_length=5, choices=WINNER_CHOICES, null=True, blank=True)
    is_closed = models.BooleanField(default=False) # To stop new bets
    
    def __str__(self):
        return self.name
    
class Bet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    cashier = models.ForeignKey(Cashier, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet_choice = models.CharField(max_length=50) # e.g., "Team A Win"
    timestamp = models.DateTimeField(auto_now_add=True)
    
    PAYOUT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
        ('CANCELLED', 'Cancelled'),
    ]
    payout_status = models.CharField(max_length=10, choices=PAYOUT_STATUS_CHOICES, default='PENDING')
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
def __str__(self):
    return f"Bet of PHP{self.amount} on {self.event.name} by {self.cashier.name}"