from django.urls import path
from .views import PlaceBetView

urlpatterns = [
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
]