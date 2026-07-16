#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

ENV_FILE="backend/.env"
APP_URL="http://localhost:8080"

if docker compose version >/dev/null 2>&1; then
    COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE=(docker-compose)
else
    echo "Error: Docker Compose is not installed." >&2
    exit 1
fi

help() {
    cat <<EOF
MatchBeforeApply — installation helper

Usage: ./install.sh <command>

Commands:
  up        Build (if needed) and start the stack → $APP_URL
  down      Stop and remove containers (database volume is kept)
  start     Start existing containers
  stop      Stop containers (without removing them)
  rebuild   Rebuild the app image and restart
  logs      Follow logs
  status    Show container status
  help      Show this menu

First run: 'up' creates $ENV_FILE from the example if missing —
fill in your keys (GOOGLE_API_KEY, SECRET_KEY, ...) and run 'up' again.
EOF
}

ensure_env() {
    if [[ ! -f "$ENV_FILE" ]]; then
        echo "Create ./backend/.env file, then run: ./install.sh up"
        exit 1
    fi
}

case "${1:-help}" in
    up)
        ensure_env
        "${COMPOSE[@]}" up -d --build
        echo "Stack is up at $APP_URL  (logs: ./install.sh logs)"
        ;;
    down)
        "${COMPOSE[@]}" down
        echo "Stack removed. Database volume 'pgdata' was kept."
        ;;
    start)
        "${COMPOSE[@]}" start
        echo "Stack started at $APP_URL"
        ;;
    stop)
        "${COMPOSE[@]}" stop
        echo "Stack stopped."
        ;;
    rebuild)
        ensure_env
        "${COMPOSE[@]}" build app
        "${COMPOSE[@]}" up -d
        echo "App rebuilt and restarted at $APP_URL"
        ;;
    logs)
        "${COMPOSE[@]}" logs -f
        ;;
    status)
        "${COMPOSE[@]}" ps
        ;;
    help|-h|--help)
        help
        ;;
    *)
        echo "Unknown command: $1" >&2
        echo
        help
        exit 1
        ;;
esac
