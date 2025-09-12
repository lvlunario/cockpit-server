from django.urls import path
from .views import PlaceBetView, EventStatsView

urlpatterns = [
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
    path('events/<int:event_id>/stats/', EventStatsView.as_view(), name='event-stats'),
]