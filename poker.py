#!/usr/bin/env python3
# Ping and VPN status checker
# Desc: Simple script to check the ping and VPN status of the servers
#       Update the servers list to add or remove servers
#       Update the interval to change the ping interval
#       Update the VPN interface name to change the VPN interface name
# Author: Badz Asterisk

import time
import socket
import requests
import subprocess
from ping3 import ping

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"

servers = {
    "": {"location": ""},
    "": {"location": ""},
    "": {"location": ""},
    "": {"location": ""},
    "": {"location": ""},
    "": {"location": ""},
}

interval = 2

def get_ping(host):
    try:
        response = ping(host, unit="ms", timeout=2)
        if response is None:
            return None, 100
        return round(response, 2), 0
    except:
        return None, 100

def get_ip_location(host):
    try:
        ip = socket.gethostbyname(host)
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
        data = resp.json()
        city = data.get("city", "Unknown")
        country = data.get("country", "Unknown")
        return f"{city}, {country}"
    except:
        return "Unknown"

def format_ping(ping_time):
    """Return fixed-width ping string with color."""
    width = 9
    if ping_time is None:
        text = "Timeout"
        return f"{GRAY}{text:<{width}}{RESET}"
    text = f"{ping_time:.2f} ms"
    if ping_time < 100:
        return f"{GREEN}{text:<{width}}{RESET}"
    elif ping_time < 200:
        return f"{YELLOW}{text:<{width}}{RESET}"
    else:
        return f"{RED}{text:<{width}}{RESET}"

def vpn_connected(interface_name="utun4"):
    """Check if VPN utun interface exists."""
    try:
        result = subprocess.run(
            ["ifconfig", interface_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

for host, details in servers.items():
    details['location'] = get_ip_location(host)

lines_to_move = 2 + 1 + 1 + len(servers)

for _ in range(lines_to_move):
    print("")

try:
    while True:
        print(f"\033[{lines_to_move}A", end="")

        system_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"System Time: {system_time}")

        vpn_status = vpn_connected()
        vpn_text = f"{GREEN}CONNECTED{RESET}" if vpn_status else f"{RED}DISCONNECTED{RESET}"
        print(f"VPN Status: {vpn_text}")

        print(f"{'Server':<30} {'Location/Region':<25} {'Ping/ms':<12} {'Packet Drops':<15}")
        print("-" * 85)

        for host, details in servers.items():
            ping_time, packet_loss = get_ping(host)
            ping_colored = format_ping(ping_time)
            packet_loss_str = f"{packet_loss}%"
            print(f"{host:<30} {details['location']:<25} {ping_colored}    {packet_loss_str:<15}")

        time.sleep(interval)
except KeyboardInterrupt:
    print("\nExiting...")
