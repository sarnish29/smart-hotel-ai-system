# Generated by Django 4.2.20 on 2025-04-27 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalized_guest_experience', '0009_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='description',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='image',
        ),
    ]
