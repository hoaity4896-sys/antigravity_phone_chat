#!/bin/bash
# Antigravity Phone Connect - Background Daemon Launcher
# Chạy server nền, không cần terminal mở suốt

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"
LOG_FILE="$PROJECT_DIR/server_log.txt"

echo "==================================================="
echo "  Antigravity Phone Connect - Background Mode"
echo "==================================================="

# Load .env
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

PORT=${PORT:-3000}

# Dừng instance cũ nếu còn chạy
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "[INFO] Đang dừng server cũ (PID $OLD_PID)..."
        kill "$OLD_PID"
        sleep 1
    fi
    rm -f "$PID_FILE"
fi

# Đảm bảo dependencies đã cài
if [ ! -d "$PROJECT_DIR/node_modules" ]; then
    echo "[INFO] Cài npm dependencies..."
    cd "$PROJECT_DIR" && npm install --silent
fi

# Lấy IP
LOCAL_IP=$(python3 -c "import socket; s=socket.socket(); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()" 2>/dev/null || echo "127.0.0.1")
TAILSCALE_IP=$(/Applications/Tailscale.app/Contents/MacOS/Tailscale ip -4 2>/dev/null || echo "")

# Xác định protocol
PROTOCOL="http"
if [ -f "$PROJECT_DIR/certs/server.key" ] && [ -f "$PROJECT_DIR/certs/server.cert" ]; then
    PROTOCOL="https"
fi

# Khởi động Node server trong nền
echo "[INFO] Khởi động server nền..."
echo "--- Server Started at $(date) ---" > "$LOG_FILE"
cd "$PROJECT_DIR"
nohup node server.js >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PID_FILE"

# Chờ server khởi động
sleep 2

# Kiểm tra server còn sống không
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "[ERROR] Server không khởi động được. Xem $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi

# Hiển thị thông tin kết nối
LOCAL_URL="$PROTOCOL://$LOCAL_IP:$PORT"
echo ""
echo "[OK] Server đang chạy (PID $SERVER_PID)"
echo "✅ Logs: $LOG_FILE"
echo ""
echo "📡 Local WiFi : $LOCAL_URL"

NOTIF_BODY="WiFi: $LOCAL_URL"

if [ -n "$TAILSCALE_IP" ]; then
    TS_URL="$PROTOCOL://$TAILSCALE_IP:$PORT"
    echo "🔒 Tailscale  : $TS_URL"
    NOTIF_BODY="$NOTIF_BODY | Tailscale: $TS_URL"
fi

echo ""
echo "Dùng stop_daemon.sh để dừng server."

# Gửi macOS notification
osascript -e "display notification \"$NOTIF_BODY\" with title \"Antigravity Phone ✅\" subtitle \"Server đang chạy | PID $SERVER_PID\""

# Mở Terminal window riêng để hiện QR — scan xong đóng đi
QR_ARGS="📡 Local WiFi|$LOCAL_URL"
if [ -n "$TAILSCALE_IP" ]; then
    QR_ARGS="$QR_ARGS" 
    osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$PROJECT_DIR' && python3 show_qr.py '📡 Local WiFi|$LOCAL_URL' '🔒 Tailscale|$TS_URL'"
end tell
EOF
else
    osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$PROJECT_DIR' && python3 show_qr.py '📡 Local WiFi|$LOCAL_URL'"
end tell
EOF
fi

