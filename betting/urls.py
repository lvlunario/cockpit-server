from django.urls import path
from .views import (
    PlaceBetView, EventStatsView, EndEventView, SetActiveEventView,
    ActiveEventView, UpdateEventStatusView
)

urlpatterns = [
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
    path('events/active/', ActiveEventView.as_view(), name='active-event'),
    path('events/<int:event_id>/stats/', EventStatsView.as_view(), name='event-stats'),
    path('events/<int:event_id>/end/', EndEventView.as_view(), name='end-event'),
    path('events/<int:event_id>/set-active/', SetActiveEventView.as_view(), name='set-active-event'),
    path('events/<int:event_id>/status/', UpdateEventStatusView.as_view(), name='update-event-status'),
]

