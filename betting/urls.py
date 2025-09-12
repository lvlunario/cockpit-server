# betting/urls.py
from django.urls import path
from .views import (
    PlaceBetView, 
    EventStatsView, 
    FinancialSummaryView, 
    EndEventView,
    SetActiveEventView,
    ActiveEventView,
    BetStatusView,
    PayoutBetView
)

urlpatterns = [
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
    path('events/<int:event_id>/stats/', EventStatsView.as_view(), name='event-stats'),
    path('reports/financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
    path('events/<int:event_id>/end/', EndEventView.as_view(), name='end-event'),
    path('events/<int:event_id>/set-active/', SetActiveEventView.as_view(), name='set-active-event'),
    path('events/active/', ActiveEventView.as_view(), name='active-event'),
    path('bets/<uuid:bet_id>/status/', BetStatusView.as_view(), name='bet-status'),
    path('bets/<uuid:bet_id>/payout/', PayoutBetView.as_view(), name='bet-payout'),
]