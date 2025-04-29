# sms_utils.py

from twilio.rest import Client
from django.conf import settings

def send_sms_reminder(phone_number, event_name, event_time):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Reminder: {event_name} is tomorrow at {event_time}.',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid  # You can store this SID if needed
