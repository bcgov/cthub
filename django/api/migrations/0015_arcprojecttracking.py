# Generated by Django 3.1.6 on 2022-01-07 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_datafleets'),
    ]

    operations = [
        migrations.CreateModel(
            name='ARCProjectTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('create_user', models.CharField(default='SYSTEM', max_length=130)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('update_user', models.CharField(max_length=130, null=True)),
                ('funding_call', models.CharField(blank=True, max_length=50, null=True)),
                ('proponent', models.CharField(blank=True, max_length=500, null=True)),
                ('reference_number', models.CharField(blank=True, max_length=50, null=True)),
                ('project_title', models.CharField(blank=True, max_length=500, null=True)),
                ('primary_location', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(blank=True, max_length=250, null=True)),
                ('arc_funding', models.IntegerField(blank=True, null=True)),
                ('funds_issued', models.IntegerField(blank=True, null=True)),
                ('start_date', models.CharField(blank=True, max_length=250, null=True)),
                ('completion_date', models.CharField(blank=True, max_length=250, null=True)),
                ('total_project_value', models.IntegerField(blank=True, null=True)),
                ('zev_sub_sector', models.CharField(blank=True, max_length=250, null=True)),
                ('on_road_off_road', models.CharField(blank=True, max_length=250, null=True)),
                ('fuel_type', models.CharField(blank=True, max_length=250, null=True)),
                ('publicly_announced', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'arc_project_tracking',
            },
        ),
    ]
