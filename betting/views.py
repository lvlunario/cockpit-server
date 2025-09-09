from django.shortcuts import render
from rest_framework import generics
from .models import Bet
from .serializers import BetSerializer

class PlaceBetView(generics.CreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

