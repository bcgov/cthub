# Generated by Django 3.2.25 on 2024-06-11 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20240611_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedvinrecord',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]