# Generated by Django 5.1.3 on 2024-11-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_event_max_participants_event_max_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_virtual',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_participants',
        ),
        migrations.AddField(
            model_name='event',
            name='max_participants',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
