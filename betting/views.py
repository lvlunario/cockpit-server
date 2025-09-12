from django.shortcuts import render
from rest_framework import generics
from .models import Bet
from .serializers import BetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .logic import calculate_event_stats

class PlaceBetView(generics.CreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

class EventStatsView(APIView):
    """
    Provides live statistics for a specific event.
    """
    
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            stats = calculate_event_stats(event)
            return Response(stats)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)