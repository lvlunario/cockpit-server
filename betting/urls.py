from django.urls import path
from .views import PlaceBetView, EventStatsView, FinancialSummaryView, EndEventView

urlpatterns = [
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
    path('events/<int:event_id>/stats/', EventStatsView.as_view(), name='event-stats'),
    path('reports/financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
    path('events/<int:event_id>/end/', EndEventView.as_view(), name='end-event'),
]