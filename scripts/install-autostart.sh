#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${PROJECT_DIR}/.venv"
UNIT_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}/systemd/user"
UNIT_FILE="${UNIT_DIR}/agent-memory-server.service"
MEMORY_BIND_HOST="${MEMORY_BIND_HOST:-127.0.0.1}"
MEMORY_SERVER_API_KEY="${MEMORY_API_KEY:-dev-key}"

if [[ ! "${MEMORY_BIND_HOST}" =~ ^(127\.0\.0\.1|0\.0\.0\.0)$ ]]; then
  echo "MEMORY_BIND_HOST must be 127.0.0.1 or 0.0.0.0." >&2
  exit 1
fi
if [[ ! "${MEMORY_SERVER_API_KEY}" =~ ^[A-Za-z0-9_-]{1,256}$ ]]; then
  echo "MEMORY_API_KEY must contain only letters, digits, underscores, or hyphens." >&2
  exit 1
fi


if [[ ! -x "${VENV_DIR}/bin/uvicorn" ]]; then
  echo "Creating virtual environment and installing the server..."
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
  if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
    echo "Unable to create the virtual environment. Install python3-venv and rerun:" >&2
    echo "  sudo apt install python3-venv" >&2
    exit 1
  fi
  "${VENV_DIR}/bin/pip" install -e "${PROJECT_DIR}[dev]"
fi

mkdir -p "${UNIT_DIR}"
cat > "${UNIT_FILE}" <<EOF
[Unit]
Description=Agent Memory Server
After=network.target

[Service]
Type=simple
WorkingDirectory=${PROJECT_DIR}
Environment=MEMORY_API_KEY=${MEMORY_SERVER_API_KEY}
Environment=MEMORY_TEST_API_KEY=test-key
Environment=MEMORY_DB_PATH=${PROJECT_DIR}/memory.db
ExecStart=${VENV_DIR}/bin/uvicorn agent_memory.main:app --host ${MEMORY_BIND_HOST} --port 8765 --no-proxy-headers
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

chmod 600 "${UNIT_FILE}"
systemctl --user daemon-reload
systemctl --user enable agent-memory-server.service
systemctl --user restart agent-memory-server.service

echo "Agent Memory Server autostart enabled."
echo "Status: systemctl --user status agent-memory-server"
echo "Logs:   journalctl --user -u agent-memory-server -f"

