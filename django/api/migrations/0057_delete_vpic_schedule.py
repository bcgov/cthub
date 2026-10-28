from django.db import migrations


def delete_vpic_schedule(apps, schema_editor):
    try:
        Schedule = apps.get_model("django_q", "Schedule")
        Schedule.objects.filter(name="vpic_batch_decode_vins").delete()
    except LookupError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0056_delete_vinpower_schedule"),
    ]

    operations = [
        migrations.RunPython(delete_vpic_schedule, migrations.RunPython.noop),
    ]
