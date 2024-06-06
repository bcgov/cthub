from django.db import models


class Description(models.Model):
    description = models.CharField(
        blank=False, db_column="description", max_length=250, null=False
    )

    class Meta:
        abstract = True


class Named(models.Model):
    name = models.CharField(
        blank=False, db_column="description", max_length=250, null=False
    )

    class Meta:
        abstract = True


class UniquelyNamed(models.Model):
    name = models.CharField(
        blank=False, db_column="description", unique=True, null=False, max_length=250
    )

    class Meta:
        abstract = True
