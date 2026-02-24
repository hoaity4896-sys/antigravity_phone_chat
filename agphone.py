#!/usr/bin/env python3
"""
agphone — Antigravity Phone Connect CLI
Hacker-style unified control panel
"""

import sys
import os
import subprocess
import socket
import time
import argparse
import signal

# ── ANSI Colors ───────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    GREEN  = "\033[32m"
    BGREEN = "\033[92m"  # bright green
    CYAN   = "\033[36m"
    BCYAN  = "\033[96m"
    RED    = "\033[31m"
    BRED   = "\033[91m"
    YELLOW = "\033[33m"
    BYELLOW= "\033[93m"
    GRAY   = "\033[90m"
    WHITE  = "\033[97m"
    BG_BLK = "\033[40m"

def g(s):  return f"{C.BGREEN}{s}{C.RESET}"   # green highlight
def c(s):  return f"{C.BCYAN}{s}{C.RESET}"    # cyan highlight
def r(s):  return f"{C.BRED}{s}{C.RESET}"     # red
def y(s):  return f"{C.BYELLOW}{s}{C.RESET}"  # yellow
def dim(s):return f"{C.DIM}{C.GRAY}{s}{C.RESET}"

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE    = os.path.join(PROJECT_DIR, ".server.pid")
LOG_FILE    = os.path.join(PROJECT_DIR, "server_log.txt")
ENV_FILE    = os.path.join(PROJECT_DIR, ".env")
TAILSCALE   = "/Applications/Tailscale.app/Contents/MacOS/Tailscale"

# ── Banner ────────────────────────────────────────────────────────────────────
BANNER = f"""{C.BGREEN}{C.BOLD}
  ▄▄▄  ▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄  ▄▄  ▄▄  ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄  ▄  ▄▄▄▄▄▄▄▄
 ██▀██ ███  ███  ███  ████  ███  ███  ███ ███  ████████ ████  ███▀ ▀█  ████████
 ██ ██ ███  ███  ████▄▄     ███▄▄███  ███▄███  ███  ███ ████  ███    █ ███
 ██▄██ ████████  ████▀▀▀▀   ███▀▀▀██  ████▀██  ████████ ████  ███    █ ████████
  ▀▀▀  ████████  ████████   ███  ████ ███  ██  ████████ ████  ███    █ ████████
{C.RESET}{C.DIM}{C.GRAY}                    P H O N E   C O N N E C T   CLI  v2.0{C.RESET}
"""

def print_banner():
    print(BANNER)

def print_separator(char="─", width=56, color=C.GRAY):
    print(f"{color}{char * width}{C.RESET}")

def print_status_line(icon, label, value, value_color=C.BCYAN):
    print(f"  {icon}  {C.DIM}{label:<14}{C.RESET}  {value_color}{value}{C.RESET}")

# ── Env loader ────────────────────────────────────────────────────────────────
def load_env():
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

# ── Network helpers ───────────────────────────────────────────────────────────
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_tailscale_ip():
    candidates = [TAILSCALE, "tailscale", "/usr/local/bin/tailscale", "/opt/homebrew/bin/tailscale"]
    for cmd in candidates:
        try:
            r = subprocess.run([cmd, "ip", "-4"], capture_output=True, text=True, timeout=5)
            ip = r.stdout.strip()
            if ip and r.returncode == 0:
                return ip
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None

def get_protocol():
    cert_key  = os.path.join(PROJECT_DIR, "certs", "server.key")
    cert_cert = os.path.join(PROJECT_DIR, "certs", "server.cert")
    return "https" if os.path.exists(cert_key) and os.path.exists(cert_cert) else "http"

# ── PID helpers ───────────────────────────────────────────────────────────────
def read_pid():
    if os.path.exists(PID_FILE):
        try:
            return int(open(PID_FILE).read().strip())
        except Exception:
            pass
    return None

def is_running(pid):
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False

# ── Spinner ───────────────────────────────────────────────────────────────────
def spinner_wait(msg, seconds=2.5, stop_event=None):
    frames = ["⠋","⠙","⠸","⠴","⠦","⠇"]
    start = time.time()
    i = 0
    while time.time() - start < seconds:
        print(f"\r  {C.BGREEN}{frames[i % len(frames)]}{C.RESET}  {C.DIM}{msg}{C.RESET}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print(f"\r  {C.BGREEN}✓{C.RESET}  {C.DIM}{msg}{C.RESET}   ")

# ── QR display ────────────────────────────────────────────────────────────────
def display_qr_block(label, url, icon="📱"):
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        print()
        print_separator()
        print(f"  {icon}  {C.BOLD}{C.WHITE}{label}{C.RESET}")
        print(f"  {C.DIM}└─{C.RESET}  {c(url)}")
        print_separator()
        # Print QR with green color
        import io
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        qr.print_ascii(invert=True)
        sys.stdout = old_stdout
        qr_text = buf.getvalue()
        for line in qr_text.splitlines():
            print(f"  {C.BGREEN}{line}{C.RESET}")
    except ImportError:
        print(f"\n  {icon}  {label}: {c(url)}")

# ── macOS notification ────────────────────────────────────────────────────────
def notify_mac(title, subtitle, body):
    try:
        script = f'display notification "{body}" with title "{title}" subtitle "{subtitle}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_start(args):
    print_banner()
    env = load_env()
    port = env.get("PORT", "3000")
    protocol = get_protocol()

    # ── Kill old instance ──
    pid = read_pid()
    if is_running(pid):
        print(f"  {y('⚡')}  Stopping existing server {dim(f'PID {pid}')} ...")
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)

    # ── Check node_modules ──
    if not os.path.exists(os.path.join(PROJECT_DIR, "node_modules")):
        print(f"  {y('📦')}  Installing npm dependencies ...")
        subprocess.run(["npm", "install", "--silent"], cwd=PROJECT_DIR, capture_output=True)

    # ── Start server ──
    print()
    print(f"  {dim('Starting Node.js server ...')}")
    with open(LOG_FILE, "w") as lf:
        lf.write(f"--- Started {time.ctime()} ---\n")

    env_copy = os.environ.copy()
    env_copy.update(env)
    with open(LOG_FILE, "a") as lf:
        proc = subprocess.Popen(
            ["node", "server.js"],
            cwd=PROJECT_DIR,
            stdout=lf, stderr=lf,
            env=env_copy
        )

    open(PID_FILE, "w").write(str(proc.pid))
    spinner_wait("Waiting for server to initialize ...", seconds=2.5)

    # ── Check alive ──
    if not is_running(proc.pid):
        print(f"\n  {r('✗')}  Server crashed. Check {LOG_FILE}")
        sys.exit(1)

    # ── Gather network info ──
    local_ip   = get_local_ip()
    ts_ip      = get_tailscale_ip()
    local_url  = f"{protocol}://{local_ip}:{port}"
    ts_url     = f"{protocol}://{ts_ip}:{port}" if ts_ip else None

    # ── Status panel ──
    print()
    print_separator("═")
    print(f"  {g('✓')}  {C.BOLD}{C.WHITE}ANTIGRAVITY PHONE CONNECT{C.RESET}  {g('ONLINE')}")
    print_separator("═")
    print_status_line("🔋", "PID",      str(proc.pid),  C.BYELLOW)
    print_status_line("📜", "Logs",     "server_log.txt", C.GRAY)
    print_status_line("🔐", "Protocol", protocol.upper(), C.BGREEN)
    print_separator()
    print_status_line("📡", "WiFi URL", local_url)
    if ts_url:
        print_status_line("🌐", "Tailscale", ts_url, C.BGREEN)
    else:
        print_status_line("🌐", "Tailscale", "not detected", C.DIM)
    print_separator("═")
    print(f"  {dim('stop →')}  {C.CYAN}python3 agphone.py stop{C.RESET}     "
          f"{dim('logs →')}  {C.CYAN}python3 agphone.py logs{C.RESET}")
    print_separator("═")

    # ── Open QR window ──
    if not args.no_qr:
        qr_args = [f"📡 Local WiFi|{local_url}"]
        if ts_url:
            qr_args.append(f"🌐 Tailscale|{ts_url}")
        qr_script = os.path.join(PROJECT_DIR, "show_qr.py")
        qr_cmd = f"cd '{PROJECT_DIR}' && python3 '{qr_script}' " + " ".join(f"'{a}'" for a in qr_args)
        try:
            subprocess.Popen(["osascript", "-e", f'''
tell application "Terminal"
    activate
    do script "{qr_cmd}"
end tell'''])
        except Exception:
            pass

    # ── Mac notification ──
    notif = local_url
    if ts_url:
        notif += f" | {ts_url}"
    notify_mac("Antigravity Phone ✅", f"PID {proc.pid} · {protocol.upper()}", notif)


def cmd_stop(args):
    print_banner()
    pid = read_pid()
    if is_running(pid):
        print(f"  {y('⚡')}  Stopping server {dim(f'PID {pid}')} ...")
        os.kill(pid, signal.SIGTERM)
        spinner_wait("Shutting down ...", seconds=1.5)
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        print(f"  {g('✓')}  Server stopped.")
        notify_mac("Antigravity Phone", "Server stopped", f"PID {pid} terminated")
    else:
        print(f"  {dim('○')}  No server running.")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)


def cmd_status(args):
    print_banner()
    pid = read_pid()
    env = load_env()
    port = env.get("PORT", "3000")
    protocol = get_protocol()
    local_ip  = get_local_ip()
    ts_ip     = get_tailscale_ip()

    running = is_running(pid)
    status_str = f"{g('● ONLINE')}" if running else f"{r('○ OFFLINE')}"

    print_separator("═")
    print(f"  {C.BOLD}{C.WHITE}STATUS{C.RESET}  {status_str}")
    print_separator("═")
    print_status_line("🔋", "PID",      str(pid) if running else "—",  C.BYELLOW)
    print_status_line("📡", "WiFi",     f"{protocol}://{local_ip}:{port}")
    print_status_line("🌐", "Tailscale",
                       f"{protocol}://{ts_ip}:{port}" if ts_ip else "not detected",
                       C.BGREEN if ts_ip else C.DIM)
    print_status_line("📜", "Log",      LOG_FILE, C.GRAY)
    print_separator("═")


def cmd_qr(args):
    env = load_env()
    port = env.get("PORT", "3000")
    protocol = get_protocol()
    local_ip  = get_local_ip()
    ts_ip     = get_tailscale_ip()

    print_banner()
    display_qr_block("Local WiFi", f"{protocol}://{local_ip}:{port}", "📡")
    if ts_ip:
        display_qr_block("Tailscale", f"{protocol}://{ts_ip}:{port}", "🌐")
    else:
        print(f"\n  {dim('Tailscale not detected.')}")
    print()
    print_separator()
    input(f"  {dim('[Press Enter to close ...]')} ")


def cmd_logs(args):
    print_banner()
    print(f"  {dim('Tailing')} {c(LOG_FILE)} {dim('— Ctrl+C to exit')}\n")
    print_separator()
    try:
        subprocess.run(["tail", "-f", LOG_FILE])
    except KeyboardInterrupt:
        print(f"\n  {dim('Stopped.')}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="agphone",
        description="Antigravity Phone Connect — hacker CLI",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""{C.BGREEN}Commands:{C.RESET}
  {c('start')}   Start server daemon (background, no terminal needed)
  {c('stop')}    Stop running server
  {c('status')}  Show server status & network info
  {c('qr')}      Display QR codes to connect phone
  {c('logs')}    Tail live server log
        """
    )
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start",  help="Start daemon")
    p_start.add_argument("--no-qr", action="store_true", help="Skip opening QR window")

    sub.add_parser("stop",   help="Stop daemon")
    sub.add_parser("status", help="Server status")
    sub.add_parser("qr",     help="Show QR codes")
    sub.add_parser("logs",   help="Tail logs")

    args = parser.parse_args()

    if args.command == "start":   cmd_start(args)
    elif args.command == "stop":  cmd_stop(args)
    elif args.command == "status":cmd_status(args)
    elif args.command == "qr":    cmd_qr(args)
    elif args.command == "logs":  cmd_logs(args)
    else:
        print_banner()
        parser.print_help()

if __name__ == "__main__":
    main()
