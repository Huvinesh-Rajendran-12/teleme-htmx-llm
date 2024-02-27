from django.urls import path
from .views import chat_view, index, stream, submit_feedback

urlpatterns = [
    path('', index, name='index'),
    path('chat/<str:session_id>', chat_view, name='chat_view'),
    path('stream/<str:session_id>', stream, name='stream'),
    path('submit_feedback/<str:session_id>', submit_feedback, name='feedback'),
]

