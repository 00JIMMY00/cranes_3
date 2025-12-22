#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
VENV_DIR="$ROOT_DIR/venv"

log() {
    echo -e "\n[setup] $1"
}

cleanup() {
    log "Shutting down services..."
    [[ -n "${BACKEND_PID:-}" ]] && kill "$BACKEND_PID" 2>/dev/null || true
    [[ -n "${FRONTEND_PID:-}" ]] && kill "$FRONTEND_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

log "Ensuring Python virtual environment exists"
if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

log "Installing backend dependencies"
pip install --upgrade pip >/dev/null
pip install -r "$ROOT_DIR/requirements.txt"

log "Applying database migrations"
python "$BACKEND_DIR/manage.py" migrate

log "Starting Django development server on http://127.0.0.1:8000"
python "$BACKEND_DIR/manage.py" runserver 0.0.0.0:8000 &
BACKEND_PID=$!

log "Installing frontend dependencies"
cd "$FRONTEND_DIR"
npm install

log "Starting Vite dev server on http://127.0.0.1:5173"
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

log "Frontend and backend are running. Press Ctrl+C to stop both."
wait "$BACKEND_PID" "$FRONTEND_PID"
