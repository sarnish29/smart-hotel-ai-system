# ledger/urls.py
from django.urls import path
from . import views

app_name = 'ledger'  # Add this line

urlpatterns = [
    path('submit/', views.submit_entry, name='submit_entry'),
    path('ledger_dashboard/', views.ledger_dashboard, name='ledger_dashboard'),
    path('view/', views.view_ledger, name='staff_view'),
]
