# Generated by Django 3.2.25 on 2024-05-16 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20240516_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goelectricrebates',
            name='flagged',
        ),
        migrations.RemoveField(
            model_name='goelectricrebates',
            name='fleet',
        ),
    ]