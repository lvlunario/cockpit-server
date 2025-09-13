# betting/serializers.py
from rest_framework import serializers
from .models import Bet, Event

class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = [
            'id',
            'event', 
            'cashier', 
            'amount', 
            'bet_choice',
            'timestamp',
            'payout_status'
        ]
        read_only_fields = ['id', 'timestamp', 'payout_status']
        
    def validate_event(self, event_instance):
        """
        Custom validation to check if the event is open for betting.
        This is the key validation check that will fix the issue.
        """
        if not event_instance.is_active or event_instance.is_closed:
            raise serializers.ValidationError("Betting is closed for this event. It is not active.")
        return event_instance