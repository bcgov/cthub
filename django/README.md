# Backend

## Database Migrations
Create migration
```bash
# Log in to the api docker
docker exec -t -i cthub_api_1 bash

# Create migration
python manage.py makemigrations

# Run the migration
python manage.py migrate

# Log into database to inspect the new table
docker exec -t -i cthub_db_1 psql -U postgres
# run this: \d <new_table_name>
```