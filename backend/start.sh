#!/usr/bin/env bash
# Simple backend start helper — activates venv (if present) and starts uvicorn
set -euo pipefail
cd "$(dirname "$0")" || exit 1
ROOT="$(pwd)"

if [ -f "$ROOT/venv/bin/activate" ]; then
	# shellcheck disable=SC1091
	. "$ROOT/venv/bin/activate"
	echo "Activated venv: $(which python)"
else
	echo "No venv found at $ROOT/venv — using system python: $(which python)"
fi

# Install requirements if missing (non-fatal)
if [ -f "$ROOT/requirements.txt" ]; then
	pip install -r "$ROOT/requirements.txt" || true
fi

# Kill any existing uvicorn processes
pkill -f uvicorn || true
sleep 1

# Start uvicorn in background
nohup uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload > "$ROOT/../backend_uvicorn.log" 2>&1 &
echo $! > "$ROOT/../backend_uvicorn.pid"
echo "Started uvicorn pid: $(cat "$ROOT/../backend_uvicorn.pid")"

echo "Tailing log (ctrl-c to stop):"
tail -n 200 -f "$ROOT/../backend_uvicorn.log"
