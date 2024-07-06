#!/bin/sh

echo "Migrate the Database at startup of project"

# Wait for few minute and run db migraiton
while ! python /usr/src/django_app/manage.py migrate --noinput 2>&1; do
    echo "Migration is in progress status"
    sleep 3
done

echo "Collect static at startup of project"

# Wait for few minute and run db migraiton
while ! python /usr/src/django_app/manage.py collectstatic --noinput 2>&1; do
    echo "collectstatic is in progress status"
    sleep 3
done

echo "Django docker is fully configured successfully."

exec "$@"
