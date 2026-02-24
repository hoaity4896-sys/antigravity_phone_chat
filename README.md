# Antigravity Phone Connect 📱

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Real-time mobile monitor và remote control cho Antigravity AI — xem và điều khiển AI từ iPhone, từ bất kỳ đâu.

> **Fork từ** [krishnakanthb13/antigravity_phone_chat](https://github.com/krishnakanthb13/antigravity_phone_chat), phân phối theo [GNU GPL v3](LICENSE).
>
> **Thay đổi bởi [@hoaity4896-sys](https://github.com/hoaity4896-sys):**
> - Tự động phát hiện **Tailscale IP** (thay thế ngrok)
> - Hiển thị **2 QR code** cùng lúc: Local WiFi và Tailscale

---

## Yêu cầu

- **macOS** với Antigravity đã cài tại `/Applications/Antigravity.app`
- **Node.js** ≥ 16
- **Python 3**
- **Tailscale** cài trên Mac và iPhone (khuyên dùng, thay ngrok)

---

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

---

## Sử dụng

### Bước 1: Mở Antigravity ở chế độ Debug

```bash
open -a Antigravity --args --remote-debugging-port=9000
```

Sau đó mở hoặc tạo 1 chat trong Antigravity.

### Bước 2: Chạy server

```bash
./start_ag_phone_connect.sh
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
