# Generated by Django 3.1.6 on 2021-11-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_ldvrebates"),
    ]

    operations = [
        migrations.CreateModel(
            name="VINDecodedInformation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_timestamp",
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
                ("create_user", models.CharField(default="SYSTEM", max_length=130)),
                ("update_timestamp", models.DateTimeField(auto_now=True, null=True)),
                ("update_user", models.CharField(max_length=130, null=True)),
                (
                    "manufacturer",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("make", models.CharField(blank=True, max_length=250, null=True)),
                ("model", models.CharField(blank=True, max_length=250, null=True)),
                ("model_year", models.IntegerField(blank=True, null=True)),
                (
                    "fuel_type_primary",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
            ],
            options={
                "db_table": "vin_decoded_information",
            },
        ),
    ]
