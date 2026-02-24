#!/bin/bash
# Antigravity Phone Connect — One-line installer
# Usage: curl -fsSL https://raw.githubusercontent.com/hoaity4896-sys/antigravity_phone_chat/master/install.sh | bash

set -e

GREEN='\033[92m'; CYAN='\033[96m'; YELLOW='\033[93m'; RED='\033[91m'; RESET='\033[0m'
ok()  { echo -e "${GREEN}✓${RESET}  $1"; }
info(){ echo -e "${CYAN}→${RESET}  $1"; }
warn(){ echo -e "${YELLOW}⚠${RESET}  $1"; }
fail(){ echo -e "${RED}✗${RESET}  $1"; exit 1; }

REPO="https://github.com/hoaity4896-sys/antigravity_phone_chat.git"
DEST="$HOME/antigravity_phone_chat"

echo ""
echo -e "${GREEN}  Antigravity Phone Connect — Installer${RESET}"
echo -e "  ──────────────────────────────────────"
echo ""

# ── Check OS ──────────────────────────────────────────────────────────────────
OS=$(uname -s)
if [[ "$OS" == "Darwin" ]]; then
    PLATFORM="macOS"
elif [[ "$OS" == "Linux" ]]; then
    PLATFORM="Linux"
else
    fail "Unsupported OS: $OS"
fi
ok "Platform: $PLATFORM"

# ── Check Git ─────────────────────────────────────────────────────────────────
command -v git &>/dev/null || fail "Git not found. Install Git first."
ok "Git found"

# ── Check Node.js ─────────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
    if [[ "$PLATFORM" == "Linux" ]]; then
        info "Installing Node.js 20..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - &>/dev/null
        sudo apt install -y nodejs &>/dev/null
        ok "Node.js installed"
    else
        fail "Node.js not found. Install from https://nodejs.org"
    fi
else
    ok "Node.js $(node --version)"
fi

# ── Check Python 3 ────────────────────────────────────────────────────────────
command -v python3 &>/dev/null || fail "Python 3 not found."
ok "Python $(python3 --version | awk '{print $2}')"

# ── Clone or update repo ──────────────────────────────────────────────────────
if [[ -d "$DEST/.git" ]]; then
    info "Updating existing install at $DEST ..."
    git -C "$DEST" pull --quiet
    ok "Updated"
else
    info "Cloning into $DEST ..."
    git clone --quiet "$REPO" "$DEST"
    ok "Cloned"
fi

cd "$DEST"

# ── npm install ───────────────────────────────────────────────────────────────
info "Installing npm packages..."
npm install --silent
ok "npm packages ready"

# ── pip: qrcode ───────────────────────────────────────────────────────────────
info "Installing Python qrcode..."
pip3 install qrcode --quiet 2>/dev/null || warn "Could not install qrcode (QR display unavailable)"
ok "qrcode installed"

# ── .env setup ───────────────────────────────────────────────────────────────
if [[ ! -f "$DEST/.env" ]]; then
    cp "$DEST/.env.example" "$DEST/.env"
    # Set working default password (template has placeholder 'your-app-password')
    sed -i.bak 's/APP_PASSWORD=.*/APP_PASSWORD=antigravity/' "$DEST/.env" && rm -f "$DEST/.env.bak"
    ok ".env created (password: antigravity)"
else
    ok ".env already exists — skipping"
fi

# ── chmod ─────────────────────────────────────────────────────────────────────
chmod +x "$DEST"/*.sh "$DEST"/*.py 2>/dev/null || true

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "  ──────────────────────────────────────"
echo -e "  ${GREEN}✓ Installation complete!${RESET}"
echo ""
echo -e "  ${CYAN}Run:${RESET}"
echo -e "    cd $DEST && python3 agphone.py"
echo ""
