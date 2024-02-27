from django.db import models
from django.db.models.fields import TextField, BooleanField
# Create your models here.

class Message(models.Model):
    session_id = TextField(default='')
    current_response_id = TextField(default='')
    user_message = models.TextField()
    llm_message = TextField(default='')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feedback = models.TextField(default="")
    is_flagged = BooleanField(default=False)

class Admin(models.Model):
    username = TextField()
    password = TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

