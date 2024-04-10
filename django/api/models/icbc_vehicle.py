"""
ICBC Vehicle Model
"""

from django.db import models

from auditable.models import Auditable


class IcbcVehicle(Auditable):
    "All vehicle models that have been added from icbc registration"
    "spreadsheet."
    make = models.CharField(blank=False, null=False, max_length=250, db_index=True)
    model_name = models.CharField(
        blank=False, max_length=250, null=False, db_index=True
    )
    model_year = models.ForeignKey(
        "ModelYear",
        related_name=None,
        on_delete=models.PROTECT,
        null=False,
        db_index=True,
    )

    class Meta:
        db_table = "icbc_vehicle"
        unique_together = [["make", "model_name", "model_year"]]
        index_together = [["make", "model_name", "model_year"]]
