# Antigravity Phone Connect 📱

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Real-time mobile monitor và remote control cho Antigravity AI — xem và điều khiển AI từ iPhone, từ bất kỳ đâu.

> **Fork từ** [krishnakanthb13/antigravity_phone_chat](https://github.com/krishnakanthb13/antigravity_phone_chat), phân phối theo [GNU GPL v3](LICENSE).
>
> **Thay đổi bởi [@hoaity4896-sys](https://github.com/hoaity4896-sys):**
> - Tự động phát hiện **Tailscale IP** (thay thế ngrok)
> - Hỗ trợ **Ubuntu / Linux** và **macOS**

---

## Yêu cầu

| | macOS | Ubuntu/Linux |
|--|-------|-------------|
| Antigravity | `/Applications/Antigravity.app` | `antigravity` trong PATH |
| Node.js ≥ 16 | ✅ | ✅ |
| Python 3 | ✅ | ✅ |
| Tailscale | App Store | `sudo apt install tailscale` |
| Desktop notifications | tích hợp sẵn | `sudo apt install libnotify-bin` |


## Cài đặt

```bash
git clone https://github.com/hoaity4896-sys/antigravity_phone_chat.git
cd antigravity_phone_chat
npm install
cp .env.example .env
```

Chỉnh `.env`:
```env
APP_PASSWORD=antigravity   # mật khẩu đăng nhập từ phone
PORT=3000
```

**Ubuntu — cài thêm:**
```bash
# Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Tailscale
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/focal.gpg | sudo apt-key add -
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/focal.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt update && sudo apt install -y tailscale libnotify-bin
sudo tailscale up
```

---

## Sử dụng

### Bước 1: Mở Antigravity ở chế độ Debug

**macOS:**
```bash
open -a Antigravity --args --remote-debugging-port=9000
```

**Ubuntu:**
```bash
antigravity . --remote-debugging-port=9000
```

Sau đó mở hoặc tạo 1 chat trong Antigravity.

### Bước 2: Chạy CLI

```bash
python3 agphone.py
```

Terminal sẽ hiện **2 QR code**:

| QR | Dùng khi |
|---|---|
| 📡 Local WiFi | iPhone cùng mạng WiFi với Mac |
| 🔒 Tailscale | Bất kỳ đâu (4G, mạng khác) — bật Tailscale trên iPhone |

### Bước 3: Kết nối iPhone

- **Tailscale (khuyên dùng):** Bật Tailscale trên iPhone → scan QR Tailscale
- **Local WiFi:** Đảm bảo cùng mạng → scan QR WiFi

Lần đầu: iPhone sẽ cảnh báo HTTPS certificate → chọn **"Advanced" → "Proceed"**

---

## HTTPS (khuyên dùng)

```bash
node generate_ssl.js
```

Khởi động lại server sau khi tạo certificate.

---

## Tính năng

- 📸 Mirror realtime giao diện Antigravity lên iPhone
- ✍️ Gửi message từ iPhone
- 🔄 Chuyển Model/Mode (Gemini/Claude/GPT, Fast/Planning)
- 📜 Xem lịch sử chat, mở chat cũ
- ➕ Tạo chat mới từ iPhone
- 🔒 Kết nối Tailscale — không cần cùng WiFi, không cần ngrok

---

## License

GNU GPL v3 — xem [LICENSE](LICENSE).

Copyright (C) 2026 **Krishna Kanth B** (@krishnakanthb13)  
Modifications Copyright (C) 2026 **hoaity4896-sys** (@hoaity4896-sys)
