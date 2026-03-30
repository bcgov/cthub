from django.db import models


class IcbcRecord(models.Model):
    create_timestamp = models.DateTimeField(auto_now_add=True, null=True)

    vin = models.TextField(null=True)

    body_style = models.TextField(null=True)

    city = models.TextField(null=True)

    electric_vehicle_flag = models.TextField(null=True)

    fleet_flag = models.TextField(null=True)

    fleet_identifier = models.BigIntegerField(null=True)

    fleet_number_of_vehicles = models.IntegerField(null=True)

    fuel_type = models.TextField(null=True)

    hybrid_vehicle_flag = models.TextField(null=True)

    licenced_gross_vehicle_weight = models.IntegerField(null=True)

    make = models.TextField(null=True)

    model = models.TextField(null=True)

    model_year = models.IntegerField(null=True)

    motorcycle_displacement_size = models.IntegerField(null=True)

    net_weight = models.IntegerField(null=True)

    odometer_reading = models.IntegerField(null=True)

    owner_giver_relationship = models.TextField(null=True)

    personal_or_commercial = models.TextField(null=True)

    policy_type = models.TextField(null=True)

    postal_code = models.TextField(null=True)

    rate_class = models.IntegerField(null=True)

    rate_class_group = models.TextField(null=True)

    snapshot_date = models.DateField(null=True)

    use_category = models.TextField(null=True)

    vehicle_purchase_date = models.DateField(null=True)

    vehicle_registration_date = models.DateField(null=True)

    vehicle_registration_number = models.IntegerField(null=True)

    vehicle_type = models.TextField(null=True)

    vin_error_code = models.TextField(null=True)

    vin_error_code_description = models.TextField(null=True)

    change_date = models.DateField(null=True)

    change = models.TextField(null=True)

    record_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "icbc"
        indexes = [
            models.Index(fields=["vin", "-create_timestamp"]),
        ]

    db_table_comment = "represents an ICBC VIN record"
