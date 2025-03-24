#!/bin/sh
echo "Waiting for PostgreSQL to start..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is up, running migrations..."
exec "$@"
