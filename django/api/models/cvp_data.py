from auditable.models import Auditable
from django.db import models


class CVPData(Auditable):

    funding_call = models.IntegerField(
        blank=False, null=False
    )

    project_identifier = models.IntegerField(
        blank=False, null=False
    )

    applicant_name = models.CharField(
        blank=False, null=False, max_length=500
    )

    rank = models.IntegerField(
        blank=True, null=True
    )

    status = models.CharField(
        blank=False, null=False, max_length=500
    )

    score = models.IntegerField(
        blank=True, null=True
    )

    vehicle_deployed = models.CharField(
        blank=False, null=False, max_length=100
    )
    
    vehicle_category = models.CharField(
        blank=False, null=False, max_length=100
    )

    drive_type = models.CharField(
        blank=False, null=False, max_length=100
    )

    vehicle_type = models.CharField(
        blank=False, null=False, max_length=100
    )

    road_class = models.CharField(
        blank=True, null=True, max_length=100
    )

    use_case = models.CharField(
        blank=True, null=True, max_length=100
    )

    make_and_model = models.CharField(
        blank=False, null=False, max_length=100
    )

    economic_region = models.CharField(
        blank=False, null=False, max_length=150
    )

    start_date = models.DateField(
        blank=True, null=True
    )

    completion_date = models.DateField(
        blank=True, null=True
    )

    project_type = models.CharField(
        blank=False, null=False, max_length=100
    )

    class_3 = models.IntegerField(
        blank=True, null=True
    )

    class_4 = models.IntegerField(
        blank=True, null=True
    )

    class_5 = models.IntegerField(
        blank=True, null=True
    )

    class_6 = models.IntegerField(
        blank=True, null=True
    )

    class_7 = models.IntegerField(
        blank=True, null=True
    )

    class_8 = models.IntegerField(
        blank=True, null=True
    )

    on_road_total = models.IntegerField(
        blank=True, null=True
    )

    off_road = models.IntegerField(
        blank=True, null=True
    )

    level_2_charger = models.IntegerField(
        blank=True, null=True
    )

    level_3_charger = models.IntegerField(
        blank=True, null=True
    )

    high_level_3_charger = models.IntegerField(
        blank=True, null=True
    )

    level_charger = models.IntegerField(
        blank=True, null=True
    )

    other_charger = models.IntegerField(
        blank=True, null=True
    )

    h2_fuelling_station = models.IntegerField(
        blank=True, null=True
    )

    charger_brand = models.CharField(
        blank=True, null=True, max_length=100
    )

    h2_fuelling_station_description = models.CharField(
        blank=True, null=True, max_length=500
    )

    ghg_emission_reduction = models.IntegerField(
        blank=True, null=True
    )

    estimated_ghg_emission_reduction = models.IntegerField(
        blank=True, null=True
    )

    funding_efficiency = models.IntegerField(
        blank=True, null=True
    )

    market_emission_reductions = models.IntegerField(
        blank=True, null=True
    )

    cvp_funding_request = models.IntegerField(
        blank=False, null=False
    )

    cvp_funding_contribution = models.IntegerField(
        blank=False, null=False
    )

    external_funding = models.IntegerField(
        blank=True, null=True
    )

    proponent_funding = models.IntegerField(
        blank=True, null=True
    )

    project_cost_initial = models.IntegerField(
        blank=False, null=False
    )

    project_cost_revised = models.IntegerField(
        blank=False, null=False
    )

    funding_source = models.CharField(
        blank=True, null=True, max_length=500
    )

    notes = models.CharField(
        blank=True, null=True, max_length=500
    )

    imhzev = models.CharField(
        blank=True, null=True, max_length=500
    )

    class Meta:
        db_table = "cvp_data"
