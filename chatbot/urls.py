from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat-api/', views.chat_api, name='chat_api'),  
]
