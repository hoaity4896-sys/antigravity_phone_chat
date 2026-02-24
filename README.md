# Antigravity Phone Connect 📱

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Real-time mobile monitor và remote control cho Antigravity AI — xem và điều khiển AI từ điện thoại, từ bất kỳ đâu.

> **Fork từ** [krishnakanthb13/antigravity_phone_chat](https://github.com/krishnakanthb13/antigravity_phone_chat), phân phối theo [GNU GPL v3](LICENSE).
>
> **Thay đổi bởi [@hoaity4896-sys](https://github.com/hoaity4896-sys):**
> - Tự động phát hiện **Tailscale IP** (không cần ngrok)
> - Hỗ trợ **macOS và Ubuntu/Linux**
> - **Interactive CLI** (`agphone.py`) thay thế các script rời

---
## ⚡ Cài đặt nhanh (1 lệnh)

```bash
curl -fsSL https://raw.githubusercontent.com/hoaity4896-sys/antigravity_phone_chat/master/install.sh | bash
```

Script tự động clone repo, cài npm packages, Python qrcode, tạo `.env`.  
Sau đó: `cd ~/antigravity_phone_chat && python3 agphone.py`

---



## Yêu cầu

| | macOS | Ubuntu/Linux |
|--|-------|-------------|
| Antigravity | `/Applications/Antigravity.app` | `antigravity` trong PATH |
| Node.js ≥ 16 | ✅ | ✅ |
| Python 3 | ✅ | ✅ |
| Tailscale | App Store | xem bên dưới |
| Desktop notifications | tích hợp sẵn | `sudo apt install libnotify-bin` |

---

## Cài đặt

```bash
git clone https://github.com/hoaity4896-sys/antigravity_phone_chat.git
cd antigravity_phone_chat
npm install
cp .env.example .env
pip3 install qrcode        # để hiện QR code trong terminal
```

Chỉnh `.env`:
```env
APP_PASSWORD=antigravity   # mật khẩu đăng nhập từ điện thoại
PORT=3000
```

### Ubuntu — cài thêm

```bash
# Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Tailscale (cách chính thức, luôn mới nhất)
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Desktop notifications (cho agphone.py)
sudo apt install -y libnotify-bin
```

---

## Sử dụng

### Bước 1: Mở Antigravity ở chế độ Debug

**macOS** — chạy lệnh hoặc dùng option `[0]` trong CLI:
```bash
open -a Antigravity --args --remote-debugging-port=9000
```

**Ubuntu:**
```bash
antigravity . --remote-debugging-port=9000
```

> Sau đó mở hoặc tạo 1 chat trong Antigravity. Server cần có chat session active.

### Bước 2: Chạy CLI

```bash
python3 agphone.py
```

Menu options:

| Key | Chức năng |
|-----|-----------|
| `0` | Mở Antigravity (Debug mode) |
| `1` | Start server (chạy nền, hiện QR inline) |
| `2` | Stop server |
| `r` | Restart server |
| `3` | Status — IP, PID, Tailscale |
| `4` | Hiện QR code bất kỳ lúc nào |
| `5` | Tail live logs |
| `q` | Thoát |

### Bước 3: Kết nối điện thoại

Sau khi start, CLI hiện **2 QR code**:

| QR | Dùng khi |
|---|---|
| 📡 Local WiFi | Điện thoại cùng mạng WiFi |
| 🌐 Tailscale | Bất kỳ đâu (4G, mạng khác) — bật Tailscale trên điện thoại |

**Lần đầu kết nối HTTPS:** điện thoại cảnh báo certificate → chọn **"Advanced" → "Proceed"** là vào được.

---

## HTTPS (khuyên dùng)

```bash
node generate_ssl.js
```

Restart server sau khi tạo certificate. Tailscale đã mã hóa end-to-end nên HTTPS là optional.

---

## Tính năng

- 📸 Mirror realtime giao diện Antigravity lên điện thoại
- ✍️ Gửi message, dừng generation từ điện thoại
- 🔄 Chuyển Model/Mode (Gemini/Claude/GPT, Fast/Planning)
- 📜 Xem lịch sử chat, mở chat cũ
- ➕ Tạo chat mới từ điện thoại
- 🌐 Kết nối qua Tailscale — không cần cùng WiFi, không cần ngrok
- 🖥️ Hỗ trợ macOS và Ubuntu/Linux

---

## License

GNU GPL v3 — xem [LICENSE](LICENSE).

Copyright (C) 2026 **Krishna Kanth B** (@krishnakanthb13)  
Modifications Copyright (C) 2026 **hoaity4896-sys** (@hoaity4896-sys)
