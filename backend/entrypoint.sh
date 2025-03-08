#!/bin/sh

# Exit script on any error
set -e  

echo "Starting entrypoint.sh..."

# Debugging: Print environment variables
echo "Database Host: $DB_HOST"
echo "Database Name: $DB_NAME"
echo "Database User: $DB_USER"

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
until mysqladmin ping -h"$DB_HOST" --silent; do
    echo "MySQL is not ready yet..."
    sleep 2
done

echo "MySQL is up! Running migrations..."

# Apply database migrations
python manage.py migrate --noinput

echo "Starting Django server..."
exec "$@"