# Generated by Django 5.0.2 on 2024-02-26 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm_app', '0003_alter_message_llm_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='current_response_id',
            field=models.TextField(default=''),
        ),
    ]
