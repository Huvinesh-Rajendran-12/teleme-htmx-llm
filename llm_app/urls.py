from django.urls import path
from .views import chat_view, index, stream

urlpatterns = [
    path('', index, name='index'),
    path('chat/<str:session_id>', chat_view, name='chat_view'),
    path('stream/<str:session_id>', stream, name='stream'),
]

