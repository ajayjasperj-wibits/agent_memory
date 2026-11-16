#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${AGENT_CLI_WORKSPACE:-/home/ajay-jasper/Projects/scola-connect}"
VENV_DIR="${AGENT_MEMORY_VENV:-$ROOT_DIR/.venv}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

if [[ ! -d "$WORKSPACE_DIR" ]]; then
  echo "AGENT_CLI_WORKSPACE does not exist: $WORKSPACE_DIR" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found" >&2
  exit 1
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "codex is required but was not found in PATH" >&2
  exit 1
fi

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Creating virtual environment: $VENV_DIR"
  if ! python3 -m venv "$VENV_DIR"; then
    echo "Could not create the virtual environment. Install it with: sudo apt install python3-venv" >&2
    exit 1
  fi
fi

PYTHON_BIN="$VENV_DIR/bin/python"

if [[ "${SKIP_INSTALL:-0}" != "1" ]]; then
  "$PYTHON_BIN" -m pip install \
    'fastapi>=0.115,<1' \
    'uvicorn[standard]>=0.30,<1' \
    'pydantic>=2.8,<3' \
    'python-multipart>=0.0.9,<1' \
    'pytest>=8' \
    'httpx>=0.27'
fi

export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export AGENT_CLI_WORKSPACE="$WORKSPACE_DIR"
export AGENT_CLI_COMMAND="${AGENT_CLI_COMMAND:-codex --ask-for-approval never exec --sandbox workspace-write}"

echo "Agent Memory UI: http://$HOST:$PORT/ui"
echo "Codex workspace: $AGENT_CLI_WORKSPACE"
echo "CLI command: $AGENT_CLI_COMMAND"

cd "$ROOT_DIR"
exec "$PYTHON_BIN" -m uvicorn agent_memory.main:app --host "$HOST" --port "$PORT" --reload
