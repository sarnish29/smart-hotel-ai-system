from django.urls import path
from . import views
from . import remainder 

app_name = 'personalized_guest_experience'

urlpatterns = [
    path('', views.personalized_home, name='personalized_home'),
    path('ai-recommendations/', views.ai_recommendations, name='ai_recommendations'),
    path('rooms/<slug:room_slug>/', views.room_detail, name='room_detail'),

    path('events/', views.event_schedule, name='event_schedule'),
    path('create-event/', views.create_event, name='create_event'), 


    path('live-events/', views.live_event_suggestions, name='live_events'),

    path('trip_planner/', views.trip_planner, name='trip_planner'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    path('surprise_me/', views.surprise_me, name='surprise_me'),

    path('send-mail-reminder/<int:event_id>/', remainder.send_mail_reminder, name='send_mail_reminder'),
    path('send-sms-reminder/<int:event_id>/', remainder.send_sms_reminder_view, name='send_sms_reminder'),

]
