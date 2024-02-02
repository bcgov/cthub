# Backend

## Database Migrations
Create migration
```bash
# Log in to the api docker
docker-compose exec api bash

# Create migration
python manage.py makemigrations

# Run the migration
python manage.py migrate

# Log into database to inspect the new table
docker-compose exec db psql -U postgres
# run this: \d <new_table_name>
```

If you need to change a migration you can back up by doing the following:
1. List the migrations to find where you want to go back to
> `python manage.py showmigrations`
2. Move migration to the appropriat state
> `python manage.py migrate --fake api 0003_name_of_migration_before_one_to_redo`
3. Delete the migration file
4. Delete table if necessary
5. Re-run migration
> `python manage.py makemigrations`


## Data Loads
Copy the spreadsheet into the _api_ docker container.
```bash
docker cp 'EV_Fast-Charging Stations_20210520.xlsx' cthub_api_1:/tmp/
```
This can also be done by temporarily placing the Excel file in the _django_ folder. This location is mounted onto the container.

Log into the docker container and run the following command.
```bash
python manage.py import_charger_rebates '/tmp/EV_Fast-Charging Stations_20210520.xlsx'
```

## Fixtures
If docker doesn't load your fixtures and the dataset dropdown list is empty use
use the same as above to load fixtures

docker-compose exec api bash
python manage.py loaddata api/fixtures/0001_add_ldv_rebates_datasets.json 

etc