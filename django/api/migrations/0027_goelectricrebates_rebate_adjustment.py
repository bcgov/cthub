# Generated by Django 3.2.25 on 2024-06-05 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_uploadedvinsfile_chunk_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='goelectricrebates',
            name='rebate_adjustment',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
