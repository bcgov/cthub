# Generated by Django 3.1.6 on 2024-03-26 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20240311_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialityusevehicleincentives',
            name='date',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
    ]