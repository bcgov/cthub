from django.db import migrations, models
from datetime import datetime

def add_region_data(apps, schema_editor):
    Regions = apps.get_model('api', 'Regions')
    
    current_timestamp = datetime.now()

    regions_data = [
        {"name": "Nechako"},
        {"name": "Northeast"},
        {"name": "Cariboo"},
        {"name": "North Coast"},
        {"name": "Vancouver Island/Coast"},
        {"name": "Mainland/Southwest"},
        {"name": "Thompson/Okanagan"},
        {"name": "Kootenay"},
        {"name": "Across BC"},
    ]
    
    for region in regions_data:
        Regions.objects.get_or_create(
            defaults={
                "create_timestamp": current_timestamp,
                "create_user": "SYSTEM",
                "update_timestamp": current_timestamp,
                "update_user": "SYSTEM",
                "name": region["name"]
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20240911_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regions',
            name='name',
            field=models.CharField(max_length=250, null=False, unique=True)
        ),
        migrations.RunPython(add_region_data),
    ]
