# DESIGN PHILOSOPHY - Antigravity Phone Connect

## Problem Statement
Developing with powerful AI models like Claude or Gemini in Antigravity often involves long "thinking" times or prolonged generation of large codebases. Developers are often "tethered" to their desks, waiting for a prompt to finish before they can review or provide the next instruction.

## The Solution: A Seamless Extension
Antigravity Phone Connect isn't a replacement for the desktop IDE; it's a **wireless viewport**. It solves the "tethering" problem by mirroring the state of the desktop session to any device on the local network.

## Design Principles

### 1. Robustness Over Precision
Selecting elements in a dynamically changing IDE like VS Code is brittle. This project prioritizes **Text-Based Selection** and **Fuzzy Matching**. Instead of looking for `.button-32x`, we look for an element that *looks like a button* and *contains the word "Gemini"*.

### 2. Zero-Impact Mirroring
The snapshot system clones the DOM before capturing. This ensures that the mirroring process doesn't interfere with the developer's cursor, scroll position, or focus on the Desktop machine.

### 3. Visual Parity (The Dark Mode Bridge)
VS Code themes have thousands of CSS variables. Instead of trying to mirror every variable perfectly, we use **Aggressive CSS Inheritance**. The frontend captures the raw HTML and wraps it in a modern, slate-dark UI that feels premium and natively mobile, regardless of the Desktop's theme.

### 4. Security-First Local Access
- **HTTPS by Default**: When SSL certificates are generated, the server automatically uses HTTPS.
- **Hybrid SSL Generation**: Tries OpenSSL first (better IP SAN support), falls back to Node.js crypto (zero dependencies).
- **Auto IP Detection**: Certificates include your local network IP addresses for better browser compatibility.
- **LAN Constraint**: The app is constrained to the local area network by default, ensuring your proprietary project snapshots aren't exposed to the public internet.

> 📚 For browser warning bypass instructions and security recommendations, see [SECURITY.md](SECURITY.md).

### 5. Resilient Error Handling
- **Optimistic Updates**: Message sending clears the input immediately and refreshes to verify.
- **No Error Popups**: Silent failures are logged but don't interrupt the user experience.
- **Memory Leak Prevention**: Centralized CDP message handling with timeout cleanup.
- **Graceful Shutdown**: Clean exit on Ctrl+C, closing all connections properly.

## Human-Centric Features

- **The "Bathroom" Use Case**: Optimized for quick checking of status while away from the desk.
- **Thought Expansion**: The generation process often "hides" the reasoning. We added remote-click relay specifically so you can "peek" into the AI's internal thoughts from your phone - both expanding AND collapsing.
- **Bi-directional Sync**: If you change the model on your Desktop, your phone updates automatically. The goal is for both devices to feel like parts of the same "brain".
- **🔒 Secure Connection**: HTTPS support removes the browser warning icon, making the experience feel more professional and trustworthy.

## Technical Trade-offs

| Decision | Rationale |
| :--- | :--- |
| Self-signed certs (not CA) | Simpler setup, works offline, no domain needed |
| Pure Node.js SSL generation | No OpenSSL dependency, works on all platforms |
| No authentication | Simplicity for LAN use; add VPN for remote access |
| Optimistic message sending | Better UX; message usually succeeds even if CDP reports issues |
| Multiple snapshot reloads | Catches UI animations that complete after initial delay |
