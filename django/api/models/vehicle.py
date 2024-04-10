from django.db import models

from auditable.models import Auditable


class Vehicle(Auditable):
    make = models.CharField(blank=False, null=False, max_length=250)
    vehicle_zev_type = models.ForeignKey(
        "ZevType", related_name=None, on_delete=models.PROTECT
    )
    vehicle_class_code = models.ForeignKey(
        "VehicleClass", related_name=None, on_delete=models.PROTECT
    )
    range = models.IntegerField()
    model_name = models.CharField(blank=False, max_length=250, null=False)
    model_year = models.ForeignKey(
        "ModelYear", related_name=None, on_delete=models.PROTECT, null=False
    )
    validation_status = models.CharField(max_length=20, null=False, default="DRAFT")
    organization = models.ForeignKey(
        "Organization", related_name=None, on_delete=models.PROTECT, null=False
    )
    weight_kg = models.DecimalField(blank=False, max_digits=6, decimal_places=0)
    credit_class = models.ForeignKey(
        "CreditClass", related_name="+", on_delete=models.PROTECT, null=True
    )
    has_passed_us_06_test = models.BooleanField(default=False)
    credit_value = models.DecimalField(null=True, decimal_places=2, max_digits=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "vehicle"
        unique_together = [["make", "model_name", "vehicle_zev_type", "model_year"]]
