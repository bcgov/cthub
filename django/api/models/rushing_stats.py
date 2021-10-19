"""
Rushing Statistics Model
"""
from django.db.models import \
    BooleanField, DecimalField, ForeignKey, Model, PROTECT


class RushingStats(Model):
    """
    Contains the rushing statistics for a player
    """
    player = ForeignKey(
        'Player',
        on_delete=PROTECT,
        null=False
    )
    att_per_game = DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True
    )
    att_total = DecimalField(
        max_digits=7,
        decimal_places=0,
        null=True
    )
    yds_total = DecimalField(
        max_digits=7,
        decimal_places=0,
        null=True
    )
    yds_avg_per_att = DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True
    )
    yds_per_game = DecimalField(
        max_digits=7,
        decimal_places=1,
        null=True
    )
    td_total = DecimalField(
        max_digits=5,
        decimal_places=0,
        null=True
    )
    rush_max = DecimalField(
        max_digits=5,
        decimal_places=0,
        null=True
    )
    rush_max_td = BooleanField(
    )
    rush_1st = DecimalField(
        max_digits=5,
        decimal_places=0,
        null=True
    )
    rush_1st_pct = DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True
    )
    rush_20_yds = DecimalField(
        max_digits=7,
        decimal_places=0,
        null=True
    )
    rush_40_yds = DecimalField(
        max_digits=7,
        decimal_places=0,
        null=True
    )
    fumbles_total = DecimalField(
        max_digits=7,
        decimal_places=0,
        null=True
    )

    class Meta:
        db_table = "rushing_stats"
