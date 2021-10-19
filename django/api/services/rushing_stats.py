"""
Services for Rushing Stats
"""
from decimal import Decimal
from api.models.player import Player
from api.models.rushing_stats import RushingStats
from api.models.team import Team


def import_from_json(data):
    """
    Translate JSON data and create records in their respective models
    """
    rows_created = 0

    for row in data:
        player_name = row.get('Player')
        # determine the player's first name and last name by looking for
        # the first space
        first_name, last_name = player_name.split(' ', 1)

        position = row.get('Pos')

        team_code = row.get('Team')
        team = Team.objects.filter(
            t_code=team_code
        ).first()

        attempts_per_game = row.get('Att/G')
        rushing_average_yards_per_attempt = row.get('Avg')
        total_attempts = row.get('Att')
        total_touchdowns = row.get('TD')
        total_yards = row.get('Yds')
        yards_per_game = total_yards = row.get('Yds/G')

        rushing_1st_downs = row.get('1st')
        rushing_1st_percentage = row.get('1st%')
        rushing_20plus_yards_each = row.get('20+')
        rushing_40plus_yards_each = row.get('40+')
        fumbles = row.get('FUM')

        longest_rush_string = str(row.get('Lng'))

        # check if the longest rush result in touchdown
        longest_rush_touchdown_result = False
        if 'T' in longest_rush_string.upper():
            longest_rush_touchdown_result = True

        # remove touchdown flag
        longest_rush = longest_rush_string.replace('T', '')
        longest_rush = Decimal(longest_rush)

        player = Player.objects.create(
            first_name=first_name,
            last_name=last_name,
            position=position,
            team=team
        )

        if player:
            RushingStats.objects.create(
                player=player,
                att_per_game=attempts_per_game,
                att_total=total_attempts,
                yds_total=total_yards,
                yds_avg_per_att=rushing_average_yards_per_attempt,
                yds_per_game=yards_per_game,
                td_total=total_touchdowns,
                rush_max=longest_rush,
                rush_max_td=longest_rush_touchdown_result,
                rush_1st=rushing_1st_downs,
                rush_1st_pct=rushing_1st_percentage,
                rush_20_yds=rushing_20plus_yards_each,
                rush_40_yds=rushing_40plus_yards_each,
                fumbles_total=fumbles
            )

            rows_created += 1

    return rows_created
