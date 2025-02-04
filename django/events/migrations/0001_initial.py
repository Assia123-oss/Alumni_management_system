# Generated by Django 5.1.3 on 2024-11-22 06:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alumni', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
                ('event_type', models.CharField(choices=[('VIRTUAL', 'Virtual'), ('ON_CAMPUS', 'On Campus'), ('HYBRID', 'Hybrid')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='event_images/')),
                ('max_participants', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_mode', models.CharField(choices=[('VIRTUAL', 'Virtual'), ('ON_CAMPUS', 'On Campus')], max_length=20)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('alumni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumni.alumni')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='events.event')),
            ],
            options={
                'unique_together': {('event', 'alumni')},
            },
        ),
    ]
