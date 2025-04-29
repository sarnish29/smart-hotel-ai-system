from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'time', 'location']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


