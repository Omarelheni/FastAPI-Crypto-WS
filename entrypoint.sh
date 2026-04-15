#!/bin/bash
# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "Waiting for the database to be ready..."
  sleep 2
done

alembic upgrade head

# Start the FastAPI application
fastapi dev main.py --host 0.0.0.0 --port 8000