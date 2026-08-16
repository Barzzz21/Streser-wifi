#!/bin/bash

G='\033[0;32m'
C='\033[0;36m'
W='\033[0m'

clear
echo -e "${C}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║            🔥 WIFISEDOT PRO - BARZZ_BOT 🔥          ║"
echo "║         Created by : @Barxzzz                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${W}"

echo -e "${G}[+] Install dependencies...${W}"
pkg update -y && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${G}[+] Jalankan WIFISEDOT PRO...${W}"
python wifisedot.py
