import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cockpit.settings')
django.setup()

from betting.models import Cashier, Event

def create_test_data():
    # Create 10 cashiers / booths
    for i in range(1, 11):
        Cashier.objects.get_or_create(station_id=f"CASHIER_{i}", defaults={'name': f"Cashier Station {i}"})
        
    # Create a test event
    Event.objects.get_or_create(name="Main Event", defaults={'start_time': datetime.now()})
    
    print("Test data created successfully.")
    
if __name__ == '__main__':
    create_test_data()