#!/bin/bash
# Simple script to run tests locally

pipenv shell >/dev/null 2>&1

echo "Checking for database and Redis server..."

# Postgres
if [ ! "$(docker ps -q -f name=db)" ]; then
    # run container
    echo "Starting postgres database..."
    docker run --name db -p 5432:5432 -d postgres:11 >/dev/null
    wait
fi

# Redis
if [ ! "$(docker ps -q -f name=redis)" ]; then
    # run container
    echo "Starting Redis server..."
    docker run --name redis -p 6379:6379 -d redis:5 >/dev/null
    wait
fi

sleep 2

echo "Done."

set +a

export DB_HOST=127.0.0.1 REDIS_URL=redis://127.0.0.1:6379/1

python manage.py test

set -a

docker rm -f db redis