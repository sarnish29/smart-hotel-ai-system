from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import Event
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import timedelta


# Email Reminder Logic
def send_email_reminder(event):
    subject = f"Reminder: {event.name} Tomorrow!"
    message = f"Don't forget! {event.name} is happening tomorrow at {event.time}. See you there!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [event.created_by.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


# SMS Reminder Logic
def send_sms_reminder(phone_number, event_name, event_time):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Reminder: {event_name} is tomorrow at {event_time}.',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid


# View for sending Email Reminder
@login_required
def send_mail_reminder(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        send_email_reminder(event)
        return HttpResponse("Email reminder sent successfully.")
    except Event.DoesNotExist:
        return HttpResponse("Event not found.", status=404)


# View for sending SMS Reminder
@login_required
def send_sms_reminder_view(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        phone_number = event.created_by.profile.phone_number if hasattr(event.created_by, 'profile') else None
        if phone_number:
            send_sms_reminder(phone_number, event.name, event.time)
            return HttpResponse("SMS reminder sent successfully.")
        else:
            return HttpResponse("User does not have a phone number.")
    except Event.DoesNotExist:
        return HttpResponse("Event not found.", status=404)
