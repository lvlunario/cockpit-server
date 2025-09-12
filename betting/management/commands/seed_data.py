from django.core.management.base import BaseCommand
from datetime import datetime
from betting.models import Cashier, Event, Bet

class Command(BaseCommand):
    help = 'Seeds the database with initial test data for 25 cashiers and a new event'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))
        
        Bet.objects.all().delete()
        self.stdout.write(self.style.WARNING('  Cleared old bet data.'))

        # Clear existing cashiers for a clean slate
        Cashier.objects.all().delete()
        self.stdout.write(self.style.WARNING('  Cleared old cashier data.'))

        # Create 25 cashiers with different types
        cashier_types = {
            'Desktop/Laptop': 10,
            'Tablet': 10,
            'Handheld': 5
        }

        total_created = 0
        for type_name, count in cashier_types.items():
            for i in range(1, count + 1):
                total_created += 1
                station_id = f"{type_name.split('/')[0].upper()}_{i}"
                cashier, created = Cashier.objects.get_or_create(
                    station_id=station_id, 
                    defaults={'name': f"{type_name} Station {i}"}
                )
                if created:
                    self.stdout.write(f'  Created {cashier.name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_created} cashiers.'))
        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))