# betting/page_urls.py
from django.urls import path
from .views import cashier_interface_view, totalizer_view, operator_dashboard_view

urlpatterns = [
    # URLs for serving the HTML pages
    path('cashier/', cashier_interface_view, name='cashier-interface'),
    path('totalizer/', totalizer_view, name='totalizer-view'),
    path('operator/', operator_dashboard_view, name='operator-dashboard'),
    path('', totalizer_view, name='home'), # Default homepage
]
