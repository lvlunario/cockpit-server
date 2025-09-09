from django.urls import path
from .views import PlaceBetView

urlpattern = [
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
]