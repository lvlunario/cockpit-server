# error logging, comment out
# import logging

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Bet, Event
from .serializers import BetSerializer
from .logic import calculate_event_stats, calculate_financial_summary, process_event_payouts

# --- API Views (These are correct) ---

class PlaceBetView(generics.CreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

class EventStatsView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            stats = calculate_event_stats(event)
            return Response(stats)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class FinancialSummaryView(APIView):
    def get(self, request):
        summary_data = calculate_financial_summary()
        return Response(summary_data)

class EndEventView(APIView):
    def post(self, request, event_id):
        winner = request.data.get('winner')
        if not winner or winner.upper() not in ['MERON', 'WALA']:
            return Response(
                {"error": "A valid 'winner' (MERON or WALA) must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            event = Event.objects.get(pk=event_id, is_active=True)
            result = process_event_payouts(event, winner.upper())
            return Response(result)
        except Event.DoesNotExist:
            return Response({"error": "Active event not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # add logging here to track unexpected errors
            # logging.error(f"Unexpected error in EndEventView: {e}") 
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SetActiveEventView(APIView):
    def post(self, request, event_id):
        try:
            Event.objects.filter(is_active=True).update(is_active=None)
            event = Event.objects.get(pk=event_id)
            event.is_active = True
            event.save()
            return Response({"status": "success", "message": f"{event.name} is now the active event."})
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class ActiveEventView(APIView):
    def get(self, request):
        try:
            event = Event.objects.get(is_active=True)
            data = {'id': event.id, 'name': event.name}
            return Response(data)
        except Event.DoesNotExist:
            return Response({"error": "No active event found"}, status=status.HTTP_404_NOT_FOUND)


# --- Template-Rendering Views (These are now corrected) ---

def cashier_interface_view(request):
    # The context dictionary is no longer needed.
    return render(request, "cashier.html")

def totalizer_view(request):
    # The context dictionary is no longer needed.
    return render(request, "totalizer.html")

def operator_dashboard_view(request):
    # The context dictionary is no longer needed.
    return render(request, "operator.html")

class BetStatusView(APIView):
    """
    Looks up a bet by its UUID to check its status and payout amount.
    """
    def get(self, request, bet_id):
        try:
            bet = Bet.objects.get(pk=bet_id)
            data = {
                'id': bet.id,
                'event': bet.event.name,
                'bet_choice': bet.bet_choice,
                'amount': bet.amount,
                'status': bet.payout_status,
                'payout_amount': bet.payout_amount
            }
            return Response(data)
        except Bet.DoesNotExist:
            return Response({"error": "Bet ticket not found"}, status=status.HTTP_404_NOT_FOUND)

class PayoutBetView(APIView):
    """
    Marks a winning bet as PAID.
    """
    def post(self, request, bet_id):
        try:
            bet = Bet.objects.get(pk=bet_id)
            if bet.payout_status == 'WON':
                bet.payout_status = 'PAID'
                bet.save()
                return Response({
                    "status": "success",
                    "message": "Bet marked as PAID.",
                    "payout_amount": bet.payout_amount
                })
            elif bet.payout_status == 'PAID':
                return Response({"error": "This bet has already been paid."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "This bet is not a winner."}, status=status.HTTP_400_BAD_REQUEST)
        except Bet.DoesNotExist:
            return Response({"error": "Bet ticket not found"}, status=status.HTTP_404_NOT_FOUND)