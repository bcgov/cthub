from django.core.management.base import BaseCommand, CommandError
from api.models.app_user import AppUser, AppToken
from django.conf import settings
from django.db import transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        app_name = options["app_name"]

        try:
            app_user = AppUser.objects.get(app_name=app_name)
            AppToken.objects.get(user=app_user).delete()
            new_token = AppToken.objects.create(user=app_user)
        except Exception:
            raise CommandError("Error resetting token")

        self.stdout.write(
            "Generated new token {} for app {}".format(new_token.key, app_name)
        )
