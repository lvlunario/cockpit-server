from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Bet, Event
from .serializers import BetSerializer
from .logic import calculate_event_stats, calculate_financial_summary, process_event_payouts

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
        
class FinancialSummaryView(APIView):
    """
    Provides a high-level financial summary of all operations.
    """
    def get(self, request):
        summary_data = calculate_financial_summary()
        return Response(summary_data)
        
def cashier_interface_view(request):
    # This view simply renders and returns the cashier.html template
    # We can pass initial data to the template here if needed in the future.
    context = {
        'event_id': 1 # For now, we hardcode the main event ID
    }
    return render(request, "cashier.html", context)


def totalizer_view(request):
    """
    This view simply serves the totalizer.html template for public display
    """
    context = {
        'event_id': 1 # Hardcoding the main event for now
    }
    return render(request, "totalizer.html", context)


class EndEventView(APIView):
    """
    API endpoint for an operator to end an event and declare a winner.
    This triggers the payout calculations for all bets on that event.
    """
    def post(self, request, event_id):
        winner = request.data.get('winner')
        if not winner or winner.upper() not in ['MERON', 'WALA']:
            return Response(
                {"error": "A valid 'winner' (MERON or WALA) must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event = Event.objects.get(pk=event_id)
            result = process_event_payouts(event, winner.upper())
            return Response(result)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)