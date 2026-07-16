#!/bin/bash

echo "Running migrations..."
cd /app/backend && python -m alembic upgrade head

# Start FastAPI first
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait until FastAPI is ready
until curl -sf http://127.0.0.1:8000/api/config; do
    echo "Waiting for FastAPI..."
    sleep 2
done

echo "FastAPI is ready — starting Caddy"

# Start Caddy (foreground, keeps container alive)
caddy run --config /app/Caddyfile