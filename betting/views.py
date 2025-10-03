from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from .models import Bet, Event
from .serializers import BetSerializer
from .logic import calculate_event_stats, process_event_payouts, calculate_financial_summary

# NEW: View for operator to change the entry status
class UpdateEventStatusView(APIView):
    def post(self, request, event_id):
        status_action = request.data.get('status')
        if status_action not in ['OPEN', 'CLOSED', 'STANDBY']:
            return Response({"error": "Invalid status action."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(pk=event_id, is_active=True)
            event.betting_status = status_action
            event.save()
            return Response({"status": "success", "message": f"Entry status changed to {status_action}"})
        except Event.DoesNotExist:
            return Response({"error": "Active event not found"}, status=status.HTTP_404_NOT_FOUND)

class PlaceBetView(generics.CreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    # UPDATED: Prevent entries unless the event status is OPEN
    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        if event.betting_status != 'OPEN':
            raise ValidationError("Entries are not open for this event.")
        serializer.save()

class EventStatsView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            stats = calculate_event_stats(event)
            return Response(stats)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class EndEventView(APIView):
    def post(self, request, event_id):
        winner = request.data.get('winner')
        if not winner or winner.upper() not in ['MERON', 'WALA', 'DRAW']:
            return Response({"error": "A valid 'winner' must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(pk=event_id, is_active=True)
            result = process_event_payouts(event, winner.upper())
            return Response(result)
        except Event.DoesNotExist:
            return Response({"error": "Active event not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

def cashier_interface_view(request):
    return render(request, "cashier.html")
def totalizer_view(request):
    return render(request, "totalizer.html")
def operator_dashboard_view(request):
    return render(request, "operator.html")

