from django.db import models
from django.db.models.fields import TextField
# Create your models here.

class Message(models.Model):
    user_message = models.TextField()
    llm_message = TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Admin(models.Model):
    username = TextField()
    password = TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

