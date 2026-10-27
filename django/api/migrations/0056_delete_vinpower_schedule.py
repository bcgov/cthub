from django.db import migrations


def delete_vinpower_schedule(apps, schema_editor):
    try:
        Schedule = apps.get_model("django_q", "Schedule")
        Schedule.objects.filter(name="vinpower_batch_decode_vins").delete()
    except LookupError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0055_remove_icbcrecord_icbc_vin_efd0d6_idx_and_more"),
    ]

    operations = [
        migrations.RunPython(delete_vinpower_schedule, migrations.RunPython.noop),
    ]
