from django.db import migrations
from datetime import datetime

def add_region_data(apps, schema_editor):
    Regions = apps.get_model('api', 'Regions')
    
    current_timestamp = datetime.now()

    regions_data = [
        {"id": 1, "name": "Nechako"},
        {"id": 2, "name": "Northeast"},
        {"id": 3, "name": "Cariboo"},
        {"id": 4, "name": "North Coast"},
        {"id": 5, "name": "Vancouver Island/Coast"},
        {"id": 6, "name": "Mainland/Southwest"},
        {"id": 7, "name": "Thompson/Okanagan"},
        {"id": 8, "name": "Kootenay"},
        {"id": 9, "name": "Across BC"},
    ]
    
    for region in regions_data:
        Regions.objects.get_or_create(
            id=region["id"],
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
        migrations.RunPython(add_region_data),
    ]
