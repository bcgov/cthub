from django.db import models


class EffectiveDates(models.Model):
    effective_date = models.DateField(blank=True, null=True)

    expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True
