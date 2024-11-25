# Generated by Django 5.1.3 on 2024-11-22 06:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumni',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graduation_year', models.IntegerField()),
                ('degree', models.CharField(choices=[('BSC', 'Bachelor of Science'), ('BA', 'Bachelor of Arts'), ('MSC', 'Master of Science'), ('PHD', 'Doctor of Philosophy')], max_length=50)),
                ('current_job', models.CharField(blank=True, max_length=200)),
                ('company', models.CharField(blank=True, max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('linkedin_profile', models.URLField(blank=True)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, upload_to='alumni_profiles/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
