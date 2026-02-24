#!/bin/bash
# Antigravity Phone Connect - Stop Daemon

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        rm -f "$PID_FILE"
        echo "✅ Server đã dừng (PID $PID)"
        osascript -e "display notification \"Server đã dừng\" with title \"Antigravity Phone Connect\""
    else
        echo "[INFO] Server không còn chạy."
        rm -f "$PID_FILE"
    fi
else
    echo "[INFO] Không tìm thấy PID. Server có thể chưa chạy."
fi
