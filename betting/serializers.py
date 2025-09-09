# betting/serializers.py
from rest_framework import serializers
from .models import Bet

class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ['event', 'cashier', 'amount', 'bet_choice']