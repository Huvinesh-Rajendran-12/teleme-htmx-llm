from django.contrib import admin
from .models import Message

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_message', 'llm_message', 'ratings', 'feedback')
admin.site.register(Message, MessageAdmin)
