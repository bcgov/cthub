from django.db import migrations, models


def populate_ldv_id(apps, schema_editor):
    LdvData = apps.get_model('api', 'LdvData')
    # assign deterministic positive ids based on current order to satisfy non-null/unique before constraint
    for idx, obj in enumerate(LdvData.objects.order_by('id'), start=1):
        obj.ldv_id = idx
        obj.save(update_fields=['ldv_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_allow_null_vin'),
    ]

    operations = [
        migrations.AddField(
            model_name='ldvdata',
            name='ldv_id',
            field=models.PositiveBigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.RunPython(populate_ldv_id, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='ldvdata',
            name='ldv_id',
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]
