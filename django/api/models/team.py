"""
Team Model
"""
from django.db.models import CharField, Model

from api.managers.team import TeamManager


class Team(Model):
    """
    Contains list of NFL teams
    * Prepending t_ to make it more distinguishable
    """
    t_code = CharField(
        blank=False,
        max_length=3,
        null=False,
        unique=True
    )
    t_name = CharField(
        blank=False,
        max_length=50,
        null=False
    )

    objects = TeamManager()

    class Meta:
        db_table = 'teams'
