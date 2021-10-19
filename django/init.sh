#!/bin/sh

python manage.py clear_database
python manage.py loaddata api/fixtures/teams.json
python manage.py load_rushing_stats api/fixtures/data.json
