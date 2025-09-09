from django.db import models
import uuid

class Cashier(models.Model):
    station_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField()
    
    def __str__(self):
        return self.name
    
class Bet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    cashier = models.ForeignKey(Cashier, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet_choice = models.CharField(max_length=50) # e.g., "Team A Win"
    timestamp = models.DateTimeField(auto_now_add=True)
    
def __str__(self):
    return f"Bet {self.id} on {self.event.name}"