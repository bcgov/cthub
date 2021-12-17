import json
from os import path
from django.core.management import BaseCommand
from api.services.public_charging import import_from_xls


class Command(BaseCommand):
    """
    This command takes in an excel file and will parse and create records
    TODO: Allow users to put in a directory as an argument so that the
    function can parse multiple files
    """
    help = 'Loads file into the public charging table'

    def add_arguments(self, parser):
        """
        Currently only takes in an excel file as a required argument
        """
        parser.add_argument(
            'xls_file', help='Filename of the xls being imported'
        )

    def handle(self, *args, **options):
        """
        Function to parse the file and pass it to the import
        service
        """
        xls_file = options.get('xls_file')

        if not path.exists(xls_file):
            self.stdout.write(self.style.ERROR(
                'Cannot find {file}. '
                'Please make sure the filename is correct.'.format(
                    file=xls_file
                )
            ))
            return False
        import_from_xls(xls_file)
        self.stdout.write(self.style.SUCCESS(
            'Import complete'
        ))
