from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Bet, Event
from .serializers import BetSerializer
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
        
def cashier_interface_view(request):
    # This view simply renders and returns the cashier.html template
    # We can pass initial data to the template here if needed in the future.
    context = {
        'event_id': 1 # For now, we hardcode the main event ID
    }
    return render(request, "cashier.html", context)