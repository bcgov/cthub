from auditable.models import Auditable
from django.db import models


class Regions(Auditable):

    name = models.CharField(blank=False, null=False, max_length=250, unique=True)

    class Meta:
        db_table = "regions"
