from django.db import models
from django.db.models.fields import TextField
# Create your models here.

class Message(models.Model):
    session_id = TextField(default='')
    user_message = models.TextField()
    llm_message = TextField(default='')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feedback = models.TextField(default="")
    ratings = models.IntegerField(default=0)

class Admin(models.Model):
    username = TextField()
    password = TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

