from django.core.management import BaseCommand
from api.services.vin_decoder import decoder

class Command(BaseCommand):
    help = 'Loads operational data'

    def handle(self, *args, **options):
        decoder()
        self.stdout.write(
            self.style.SUCCESS(
                'Decoding Completed!'
            )
        )
        