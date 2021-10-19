"""
Command line function to import a JSON file into their respective
Rushing Stats Models
"""
import json
from os import path
from django.core.management import BaseCommand

from api.services.rushing_stats import import_from_json


class Command(BaseCommand):
    """
    This command takes in a json file and will parse and create records
    for players and their rushing stats
    TODO: Allow users to put in a directory as an argument so that the
    function can parse multiple json files
    """
    help = 'Loads JSON file into the players and rushing_stats table'

    def add_arguments(self, parser):
        """
        Currently only takes in a json file as a required argument
        """
        parser.add_argument(
            'json_file', help='Filename of the JSON being imported'
        )

    def handle(self, *args, **options):
        """
        Function to parse the json file and pass it to the import
        service
        """
        json_file = options.get('json_file')

        if not path.exists(json_file):
            self.stdout.write(self.style.ERROR(
                'Cannot find {file}. '
                'Please make sure the filename is correct.'.format(
                    file=json_file
                )
            ))
            return False

        with open(json_file, 'r') as file:
            try:
                data = json.load(file)
            except Exception as error:
                self.stdout.write(self.style.ERROR(
                    '{file} is not a valid JSON file. '
                ))
                return False

            rows_created = import_from_json(data)
            self.stdout.write(self.style.SUCCESS(
                '{number} rows have been imported into the database.'.format(
                    number=rows_created
                )
            ))
