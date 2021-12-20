from django.db import models


class DisplayOrder(models.Model):
    display_order = models.IntegerField()

    class Meta:
        abstract = True
