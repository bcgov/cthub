# Generated by Django 3.1.6 on 2024-02-23 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_auto_20231201_2301"),
    ]

    operations = [
        migrations.CreateModel(
            name="Permission",
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
                ("description", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "db_table": "permission",
            },
        ),
        migrations.CreateModel(
            name="User",
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
                ("idir", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="UserPermission",
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
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permission",
                        to="api.permission",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to="api.user",
                    ),
                ),
            ],
            options={
                "db_table": "user_permission",
            },
        ),
        migrations.DeleteModel(
            name="WhitelistedUsers",
        ),
    ]
