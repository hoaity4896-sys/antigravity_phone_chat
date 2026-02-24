#!/usr/bin/env python3
"""
agphone — Antigravity Phone Connect
Interactive CLI menu
"""

import sys
import os
import subprocess
import socket
import time
import signal

# ── ANSI ─────────────────────────────────────────────────────────────────────
R = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
G = "\033[92m"; C = "\033[96m"; Y = "\033[93m"
RED = "\033[91m"; W = "\033[97m"; GR = "\033[90m"

def g(s): return f"{G}{s}{R}"
def c(s): return f"{C}{s}{R}"
def y(s): return f"{Y}{s}{R}"
def r(s): return f"{RED}{s}{R}"
def dim(s): return f"{DIM}{GR}{s}{R}"

# ── Config ────────────────────────────────────────────────────────────────────
DIR      = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(DIR, ".server.pid")
LOG_FILE = os.path.join(DIR, "server_log.txt")
ENV_FILE = os.path.join(DIR, ".env")
TS_CMD   = "/Applications/Tailscale.app/Contents/MacOS/Tailscale"

BANNER = f"""{G}{BOLD}
  ░█████╗░░██████╗░  ██████╗░██╗  ██╗░█████╗░███╗░░██╗███████╗
  ██╔══██╗██╔════╝░  ██╔══██╗██║  ██║██╔══██╗████╗░██║██╔════╝
  ███████║██║░░██╗░  ██████╔╝███████║██║░░██║██╔██╗██║█████╗░░
  ██╔══██║██║░░╚██╗  ██╔═══╝░██╔══██║██║░░██║██║╚████║██╔══╝░░
  ██║░░██║╚██████╔╝  ██║░░░░░██║░░██║╚█████╔╝██║░╚███║███████╗
  ╚═╝  ╚═╝░╚═════╝░  ╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝╚══════╝{R}
  {dim('Antigravity Phone Connect  ·  CLI v2.0')}
"""

SEP = f"{GR}{'─'*54}{R}"

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_env():
    env = {}
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close(); return ip
    except: return "127.0.0.1"

def tailscale_ip():
    for cmd in [TS_CMD, "tailscale", "/opt/homebrew/bin/tailscale"]:
        try:
            r = subprocess.run([cmd, "ip", "-4"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
        except: continue
    return None

def protocol():
    return "https" if os.path.exists(os.path.join(DIR, "certs/server.key")) else "http"

def read_pid():
    try: return int(open(PID_FILE).read().strip())
    except: return None

def alive(pid):
    if not pid: return False
    try: os.kill(pid, 0); return True
    except: return False

def notify(title, msg):
    try:
        subprocess.run(["osascript", "-e",
            f'display notification "{msg}" with title "{title}"'], capture_output=True)
    except: pass

def spinner(msg, secs=2.5):
    frames = ["⠋","⠙","⠸","⠴","⠦","⠇"]
    t = time.time(); i = 0
    while time.time() - t < secs:
        print(f"\r  {G}{frames[i%len(frames)]}{R}  {dim(msg)}", end="", flush=True)
        time.sleep(0.08); i += 1
    print(f"\r  {g('✓')}  {dim(msg)}   ")

def print_qr(label, url, icon="📱"):
    try:
        import qrcode, io
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(url); qr.make(fit=True)
        print(f"\n{SEP}\n  {icon}  {BOLD}{W}{label}{R}\n  {dim('└─')}  {c(url)}\n{SEP}")
        buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
        qr.print_ascii(invert=True); sys.stdout = old
        for line in buf.getvalue().splitlines():
            print(f"  {G}{line}{R}")
    except ImportError:
        print(f"\n  {icon}  {label}: {c(url)}")

def urls():
    env = load_env()
    port = env.get("PORT", "3000")
    proto = protocol()
    lip = local_ip()
    tip = tailscale_ip()
    return proto, port, lip, tip

# ── Actions ───────────────────────────────────────────────────────────────────
def do_start():
    env = load_env()
    port = env.get("PORT", "3000")
    proto = protocol()

    pid = read_pid()
    if alive(pid):
        print(f"\n  {y('⚡')}  Stopping old server {dim(f'PID {pid}')} ...")
        os.kill(pid, signal.SIGTERM); time.sleep(1)

    if not os.path.exists(os.path.join(DIR, "node_modules")):
        print(f"  {y('📦')}  Installing npm packages ...")
        subprocess.run(["npm", "install", "--silent"], cwd=DIR, capture_output=True)

    print(f"\n  {dim('Starting server ...')}")
    with open(LOG_FILE, "w") as lf:
        lf.write(f"--- {time.ctime()} ---\n")
    env_copy = os.environ.copy(); env_copy.update(env)
    with open(LOG_FILE, "a") as lf:
        proc = subprocess.Popen(["node", "server.js"], cwd=DIR, stdout=lf, stderr=lf, env=env_copy)
    open(PID_FILE, "w").write(str(proc.pid))
    spinner("Initializing ...", 2.5)

    if not alive(proc.pid):
        print(f"\n  {r('✗')}  Server failed. Run option [5] to see logs.")
        return

    lip = local_ip(); tip = tailscale_ip()
    local_url = f"{proto}://{lip}:{port}"
    ts_url    = f"{proto}://{tip}:{port}" if tip else None

    print(f"\n{SEP}")
    print(f"  {g('●')}  {BOLD}SERVER ONLINE{R}  {dim(f'PID {proc.pid}')}")
    print(SEP)
    print(f"  📡  {dim('WiFi     ')}  {c(local_url)}")
    if ts_url: print(f"  🌐  {dim('Tailscale')}  {g(ts_url)}")
    else:      print(f"  🌐  {dim('Tailscale')}  {dim('not detected')}")
    print(SEP)

    # Show QR inline
    print_qr("Local WiFi", local_url, "📡")
    if ts_url: print_qr("Tailscale", ts_url, "🌐")

    notif_msg = local_url + (f" | {ts_url}" if ts_url else "")
    notify("Antigravity Phone ✅", notif_msg)


def do_stop():
    pid = read_pid()
    if alive(pid):
        print(f"\n  {y('⚡')}  Stopping server {dim(f'PID {pid}')} ...")
        os.kill(pid, signal.SIGTERM)
        spinner("Shutting down ...", 1.5)
        try: os.remove(PID_FILE)
        except: pass
        print(f"  {g('✓')}  Stopped.")
        notify("Antigravity Phone", "Server stopped")
    else:
        print(f"\n  {dim('○  No server running.')}")
        try: os.remove(PID_FILE)
        except: pass


def do_status():
    pid = read_pid()
    running = alive(pid)
    proto, port, lip, tip = urls()
    status = f"{g('● ONLINE')}" if running else f"{r('○ OFFLINE')}"
    print(f"\n{SEP}")
    print(f"  STATUS   {status}  {dim(f'PID {pid}') if running else ''}")
    print(SEP)
    print(f"  📡  {dim('WiFi     ')}  {c(f'{proto}://{lip}:{port}')}")
    print(f"  🌐  {dim('Tailscale')}  {g(f'{proto}://{tip}:{port}') if tip else dim('not detected')}")
    print(f"  📜  {dim('Logs     ')}  {dim(LOG_FILE)}")
    print(SEP)


def do_qr():
    proto, port, lip, tip = urls()
    print_qr("Local WiFi", f"{proto}://{lip}:{port}", "📡")
    if tip: print_qr("Tailscale",  f"{proto}://{tip}:{port}", "🌐")
    else:   print(f"\n  {dim('Tailscale not detected.')}")
    print(f"\n{SEP}")
    input(f"  {dim('[Press Enter to go back ...]')} ")


def do_logs():
    print(f"\n  {dim('Tailing')} {c(LOG_FILE)} {dim('— Ctrl+C to stop')}\n{SEP}")
    try: subprocess.run(["tail", "-f", LOG_FILE])
    except KeyboardInterrupt: print(f"\n  {dim('Stopped.')}")


def do_open_antigravity():
    print(f"\n  {dim('Launching Antigravity in Debug mode ...')}")
    try:
        subprocess.Popen(["open", "-a", "Antigravity", "--args", "--remote-debugging-port=9000"])
        spinner("Waiting for launch ...", 3)
        print(f"  {g('✓')}  Antigravity launched. Open a chat, then {c('[1] Start Server')}.")
    except Exception as e:
        print(f"  {r('✗')}  {e}")

# ── Main menu loop ────────────────────────────────────────────────────────────
def menu():
    os.system("clear")
    print(BANNER)

    while True:
        # Live status badge
        pid = read_pid()
        badge = f"{g('● ONLINE')}" if alive(pid) else f"{r('○ OFFLINE')}"

        print(f"\n{SEP}")
        print(f"  {BOLD}MENU{R}  {badge}")
        print(SEP)
        print(f"  {c('[0]')}  {BOLD}Open Antigravity{R} (Debug mode){dim(' ← start here')}")
        print(f"  {c('[1]')}  {BOLD}Start{R} server")
        print(f"  {c('[2]')}  {BOLD}Stop{R} server")
        print(f"  {c('[3]')}  {BOLD}Status{R} & network info")
        print(f"  {c('[4]')}  Show {BOLD}QR codes{R}")
        print(f"  {c('[5]')}  Tail {BOLD}logs{R}")
        print(f"  {c('[q]')}  Quit")
        print(SEP)

        try:
            choice = input(f"  {dim('Choose')} › ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {dim('Bye.')}\n"); break

        if   choice == "0": do_open_antigravity()
        elif choice == "1": do_start()
        elif choice == "2": do_stop()
        elif choice == "3": do_status()
        elif choice == "4": do_qr()
        elif choice == "5": do_logs()
        elif choice in ("q", "quit", "exit"):
            print(f"\n  {dim('Bye.')}\n"); break
        else:
            print(f"\n  {dim('Unknown option.')}")

        if choice not in ("4", "5", "q", "quit", "exit"):
            input(f"\n  {dim('[Enter to continue ...]')} ")
            os.system("clear")
            print(BANNER)

if __name__ == "__main__":
    menu()
