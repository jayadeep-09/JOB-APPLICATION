from django.urls import path
from . import views

urlpatterns = [
    path('api/upload/', views.upload_resume, name='chatbot_upload'),
    path('api/chat/', views.chat_message, name='chatbot_chat'),
    path('api/history/', views.get_history, name='chatbot_history'),
]
