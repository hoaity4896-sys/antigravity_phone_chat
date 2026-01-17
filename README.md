# Antigravity Phone Connect 📱

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Antigravity Phone Connect** is a high-performance, real-time mobile monitor and remote control for your Antigravity AI sessions. It allows you to step away from your desk while keeping full sight and control over your AI's thinking process and generations.

![Antigravity Phone Connect](./assets/hero_showcase.png)

**Note:** This project is a refined fork/extension based on the original [Antigravity Shit-Chat](https://github.com/gherghett/Antigravity-Shit-Chat) by gherghett.

---

## 🚀 Quick Start

### Windows

1.  **Double-click `start_ag_phone_connect.bat`**
    The script will:
    - Verify Node.js is installed.
    - Automatically install dependencies (`npm install`) if they are missing.
    - Detect SSL certificates and show `https://` or `http://` accordingly.
    - Display your **exact IP Address** (e.g., `https://192.168.1.5:3000`).
    - Provide tips for context menu setup and HTTPS enablement.

2.  **Connect Your Phone**
    - Ensure your phone is on the **same Wi-Fi network** as your PC.
    - Open your mobile browser and enter the **URL shown in the terminal**.
    - If using HTTPS: Accept the self-signed certificate warning on first visit.

3.  **Launch Antigravity** (if not already running)
    - **Recommended**: Run **`install_context_menu.bat`** and select **[1] Install**. Then, simply right-click any project folder and select **"Open with Antigravity (Debug)"**.
    - Otherwise, run manually: `antigravity . --remote-debugging-port=9000`

---

### macOS / Linux

1.  **Run the launcher script**
    ```bash
    chmod +x start_ag_phone_connect.sh
    ./start_ag_phone_connect.sh
    ```
    The script will:
    - Verify Node.js is installed.
    - Automatically install dependencies.
    - Detect SSL certificates and display the appropriate protocol.
    - Display your **exact IP Address**.
    - *(Linux only)* Provide tips for Nautilus/GNOME context menu management.

2.  **Connect Your Phone**
    - Ensure your phone is on the **same Wi-Fi network**.
    - Open your mobile browser and enter the **URL shown in the terminal**.

3.  **Launch Antigravity** (if not already running)
    ```bash
    antigravity . --remote-debugging-port=9000
    ```

---

## 🔒 Enabling HTTPS (Recommended)

For a secure connection without the browser warning icon:

### Option 1: Command Line
```bash
node generate_ssl.js
```
- Uses **OpenSSL** if available (includes your IP in certificate)
- Falls back to **Node.js crypto** if OpenSSL not found
- Creates certificates in `./certs/` directory

### Option 2: Web UI
1. Start the server on HTTP
2. Look for the yellow **"⚠️ Not Secure"** banner
3. Click **"Enable HTTPS"** button
4. Restart the server when prompted

### After Generating:
1. **Restart the server** - it will automatically detect and use HTTPS.
2. **On your phone's first visit**:
   - You'll see a security warning (normal for self-signed certs).
   - Tap **"Advanced"** → **"Proceed to site"**.
   - The warning won't appear again!

---

### macOS: Adding Right-Click "Quick Action" (Optional)

Since macOS requires Automator for context menu entries, follow these steps manually:

1.  Open **Automator** (Spotlight → type "Automator").
2.  Click **File → New** and select **Quick Action**.
3.  At the top, set:
    - "Workflow receives current" → **folders**
    - "in" → **Finder**
4.  In the left sidebar, search for **"Run Shell Script"** and drag it to the right pane.
5.  Set "Shell" to `/bin/zsh` and "Pass input" to **as arguments**.
6.  Paste this script:
    ```bash
    cd "$1"
    antigravity . --remote-debugging-port=9000
    ```
7.  **Save** the Quick Action with a name like `Open with Antigravity (Debug)`.
8.  Now you can right-click any folder in Finder → **Quick Actions → Open with Antigravity (Debug)**.

---

## ✨ Features

- **🔒 HTTPS Support**: Secure connections with self-signed SSL certificates.
- **Real-Time Mirroring**: 1-second polling interval for near-instant sync.
- **Remote Control**: Send messages, stop generations, and switch Modes (Fast/Planning) or Models (Gemini/Claude/GPT) directly from your phone.
- **Thought Expansion**: Tap on "Thinking..." or "Thought" blocks on your phone to remotely expand/collapse them.
- **Smart Sync**: Bi-directional synchronization ensures your phone always shows the current Model and Mode selected on your desktop.
- **Premium Mobile UI**: A sleek, dark-themed interface optimized for touch interaction.
- **Context Menu Management**: Dedicated scripts to **Install, Remove, Restart, or Backup** your Right-Click integrations.
- **Health Monitoring**: Built-in `/health` endpoint for server status checks.
- **Graceful Shutdown**: Clean exit on Ctrl+C, closing all connections properly.
- **Zero-Config**: The launch scripts handle the heavy lifting of environment setup.

---

## 📂 Documentation

For more technical details, check out:
- [**Code Documentation**](CODE_DOCUMENTATION.md) - Architecture, Data Flow, and API.
- [**Security Guide**](SECURITY.md) - HTTPS setup, certificate warnings, and security model.
- [**Design Philosophy**](DESIGN_PHILOSOPHY.md) - Why it was built this way.
- [**Contributing**](CONTRIBUTING.md) - Guidelines for developers.

---

## License

Licensed under the [GNU GPL v3](LICENSE).  
Copyright (C) 2026 **Krishna Kanth B** (@krishnakanthb13)
