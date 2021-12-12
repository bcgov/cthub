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
docker exec -t -i cthub_db_1 psql -U postgres
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