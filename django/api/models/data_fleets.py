from auditable.models import Auditable
from django.db import models


class DataFleets(Auditable):
    current_stage = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    rebate_value = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    legal_name_of_organization_fleet = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        unique=False
    )

    business_category = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    city = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    postal_code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    applicant_first_name = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    applicant_last_name = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    email_address = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    fleet_size_all = models.IntegerField(
        blank=True,
        null=True
    )

    fleet_size_light_duty = models.IntegerField(
        blank=True,
        null=True
    )

    total_number_of_evs = models.IntegerField(
        blank=True,
        null=True
    )

    total_number_of_light_duty_evs = models.IntegerField(
        blank=True,
        null=True
    )

    phev = models.IntegerField(
        blank=True,
        null=True
    )

    evse = models.IntegerField(
        blank=True,
        null=True
    )

    average_daily_travel_distance = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    component_being_applyied_for = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    estimated_cost = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    type_of_charger_being_installing = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    number_of_Level_2_Charging_Stations_being_applying_for = models.IntegerField(
        blank=True,
        null=True
    )

    number_of_level_3_dc_fast_charging_stations_being_applying_for = models.IntegerField(
        blank=True,
        null=True
    )

    application_form_fleets_completion_date_time = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    pre_approval_date = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )

    deadline = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    application_number = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    potential_rebate = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=False
    )


    class Meta:
        db_table = "data_fleets"
