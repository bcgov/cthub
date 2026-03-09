from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0046_auto_20250903_1745"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ldvdata",
            name="vin",
            field=models.CharField(max_length=17, blank=True, null=True),
        ),
    ]
