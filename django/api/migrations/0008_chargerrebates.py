# Generated by Django 3.1.6 on 2021-12-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_datasets'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargerRebates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('create_user', models.CharField(default='SYSTEM', max_length=130)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('update_user', models.CharField(max_length=130, null=True)),
                ('organization', models.CharField(blank=True, max_length=250, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=200, null=True)),
                ('number_of_fast_charging_stations', models.IntegerField(blank=True, null=True)),
                ('in_service_date', models.CharField(blank=True, max_length=100, null=True)),
                ('expected_in_service_date', models.DateField(blank=True, null=True)),
                ('announced', models.CharField(blank=True, max_length=200, null=True)),
                ('rebate_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('notes', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'charger_rebates',
            },
        ),
    ]