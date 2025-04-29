from django.core.management.base import BaseCommand
from personalized_guest_experience.models import Event  # Update if your Event model is elsewhere
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deletes past events from the database'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        past_events = Event.objects.filter(time__lt=now)
        count = past_events.count()
        past_events.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} past events'))
