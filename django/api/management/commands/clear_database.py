"""
Command line to clear the databases related to rushing stats
"""
from django.core.management import BaseCommand

from api.models.player import Player
from api.models.rushing_stats import RushingStats
from api.models.team import Team


class Command(BaseCommand):
    """
    This command line doesn't take any arguments and will clear Teams, Players
    and Rushing stats
    """
    help = 'Clears the Rushing stats and related tables'

    def handle(self, *args, **options):
        RushingStats.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            'Rushing stats Table has been cleared'
        ))

        Player.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            'Players Table has been cleared'
        ))

        Team.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            'Teams Table has been cleared'
        ))
