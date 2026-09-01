#!/usr/bin/env bash
set -euo pipefail

APP_MODULE="calculator:app"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if [ -f ".venv/bin/activate" ]; then
  . ".venv/bin/activate"
  PYTHON="${PYTHON:-python}"
else
  PYTHON="${PYTHON:-python3}"
fi

printf 'Starting calculator app on http://%s:%s\n' "$HOST" "$PORT"
exec "$PYTHON" -m uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --reload
