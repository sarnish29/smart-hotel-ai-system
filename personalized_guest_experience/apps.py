from django.apps import AppConfig

class PersonalizedGuestExperienceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalized_guest_experience'

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from .tasks import send_event_reminders

        scheduler = BackgroundScheduler()
        scheduler.add_job(send_event_reminders, 'interval', hours=6)  # check every 6 hours
        scheduler.start()
