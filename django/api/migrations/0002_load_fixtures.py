"""
Manually created to automate importing of the initial data
"""
import os
from api import settings

from django.db import migrations


def database_forward(_apps, _schema_editor):
    if not settings.TESTING:
        os.system('python manage.py clear_database')
        os.system('python manage.py loaddata api/fixtures/teams.json')
        os.system('python manage.py load_rushing_stats api/fixtures/data.json')


def database_reverse(_apps, _schema_editor):
    if not settings.TESTING:
        os.system('python manage.py clear_database')


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(database_forward, database_reverse),
    ]
