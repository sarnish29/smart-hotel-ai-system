# personalized_guest_experience/tasks.py

from datetime import timedelta
from django.utils import timezone
from .models import Event
from .remainder import send_email_reminder, send_sms_reminder

def send_event_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)
    events = Event.objects.filter(time__date=tomorrow)

    for event in events:
        try:
            # Send Email Reminder
            send_email_reminder(event.id)

            # Send SMS Reminder
            send_sms_reminder(event.id)

            print(f"Reminders sent for event: {event.name}")

        except Exception as e:
            print(f"Error sending reminders for event {event.name}: {str(e)}")
