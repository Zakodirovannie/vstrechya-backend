#!/bin/bash
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
until python manage.py makemigrations
do
  echo "Waiting for making migrations"
  sleep 2
done
until python manage.py migrate
do
  echo "Waiting for db to be ready..."
  sleep 2
done
exec "$@"
