from django.core.management.base import BaseCommand
from datetime import datetime
from betting.models import Cashier, Event

class Command(BaseCommand):
    help = 'Seeds the databse with initial test data for cashiers and events'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))
        
        # Create 10 cashiers / booths
        for i in range(1, 11):
            cashier, created = Cashier.objects.get_or_create(station_id=f"CASHIER_{i}", defaults={'name': f"Cashier Station {i}"})
            if created:
                self.stdout.write(f' Created {cashier.name}')
            
        # Create a test event
        event, created = Event.objects.get_or_create(name="Main Event", defaults={'start_time': datetime.now()})
        if created:
            self.stdout.write(f' Created event: {event.name}')
        
        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))