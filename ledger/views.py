from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LedgerEntry
from .forms import LedgerEntryForm
from django.utils import timezone
from datetime import timedelta

# Helpers
def is_staff(user):
    return user.groups.filter(name='Staff').exists()

def is_admin(user):
    return user.is_superuser

# --- Ledger Dashboard for Guest ---
@login_required
def ledger_dashboard(request):
    entries = LedgerEntry.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'ledger/ledger_dashboard.html', {'entries': entries})

# --- Guest Submit Feedback/Complaint ---
@login_required
def submit_entry(request):
    if request.method == 'POST':
        form = LedgerEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.timestamp = timezone.now()
            print(f"[DEBUG] New entry timestamp: {entry.timestamp}")  
            entry.save()
            return redirect('ledger:ledger_dashboard')  
    else:
        form = LedgerEntryForm()
    return render(request, 'ledger/submit_entry.html', {'form': form})

# --- Staff/Admin View Ledger ---
@login_required
@user_passes_test(lambda u: is_staff(u) or is_admin(u))
def view_ledger(request):
    entries = LedgerEntry.objects.all().order_by('-timestamp')
    
    # Validate ledger integrity
    tampering_alert = False
    if not LedgerEntry.validate_ledger():
        tampering_alert = True  # Set the alert if ledger is broken

    return render(request, 'ledger/view_ledger.html', {
        'entries': entries,
        'tampering_alert': tampering_alert,
    })
