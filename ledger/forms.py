from django import forms
from .models import LedgerEntry

class LedgerEntryForm(forms.ModelForm):
    class Meta:
        model = LedgerEntry
        fields = ['message', 'entry_type']
