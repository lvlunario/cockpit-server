"""
URL configuration for cockpit project.
"""
from django.contrib import admin
from django.urls import path, include
from betting.views import cashier_interface_view, totalizer_view, operator_dashboard_view

urlpatterns = [
    # Path for the Django admin site
    path('admin/', admin.site.urls),

    # This correctly sends all API requests to your betting app's urls.py
    path('api/', include('betting.urls')),

    # These are the paths for your HTML pages
    path('cashier/', cashier_interface_view, name='cashier-interface'),
    path('totalizer/', totalizer_view, name='totalizer-view'),
    path('operator/', operator_dashboard_view, name='operator-dashboard'),
    path('', totalizer_view, name='home'), # Sets the totalizer as the homepage
]

