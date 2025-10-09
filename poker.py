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
    "sslvpn.traxtech.com": {"location": ""},
    "traxtech.com": {"location": ""},
    "b2b.veraction.com": {"location": ""},
    "ttsm-002-console.traxtech.com": {"location": ""},
    "speedtest.ph": {"location": ""},
    "speedtest.com.sg": {"location": ""},
    "speedtest.london.linode.com": {"location": ""},
}
interval = 2
ROLLING_WINDOW = 50
ping_column_width = 16

ping_history = {host: [] for host in servers}


def get_ping(host):
    """Return latency in ms or None if timed out."""
    try:
        response = ping(host, unit="ms", timeout=2)
        if response is None:
            return None
        return round(response, 2)
    except:
        return None


def get_ip_location(host):
    """Get server location based on IP address."""
    try:
        ip = socket.gethostbyname(host)
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
        data = resp.json()
        city = data.get("city", "Unknown")
        country = data.get("country", "Unknown")
        return f"{city}, {country}"
    except:
        return "Unknown"


def format_ping(ping_time, width=ping_column_width):
    """Return fixed-width ping string with color, keeping alignment."""
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

# Update server locations once at startup
for host, details in servers.items():
    details['location'] = get_ip_location(host)

lines_to_move = 2 + 1 + 1 + len(servers)

for _ in range(lines_to_move):
    print("")

try:
    while True:
        print(f"\033[{lines_to_move}A", end="")
        system_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\033[KSystem Time: {system_time}")

        # VPN status
        vpn_status = vpn_connected()
        vpn_text = f"{GREEN}CONNECTED{RESET}" if vpn_status else f"{RED}DISCONNECTED{RESET}"
        print(f"\033[KVPN Status: {vpn_text}")

        # Table header
        print(f"\033[K{'Server':<30} {'Location/Region':<25} {'Ping/ms':<{ping_column_width}} {'Packet Drops':<15}")
        print("-" * 85)

        for host, details in servers.items():
            ping_time = get_ping(host)
            ping_history[host].append(1 if ping_time is not None else 0)
            if len(ping_history[host]) > ROLLING_WINDOW:
                ping_history[host].pop(0)
            packet_loss = 100 * (1 - sum(ping_history[host]) / len(ping_history[host]))
            ping_colored = format_ping(ping_time)
            packet_loss_str = f"{packet_loss:.1f}%"
            print(f"{host:<30} {details['location']:<25} {ping_colored} {packet_loss_str:<15}")

        time.sleep(interval)

except KeyboardInterrupt:
    print("\nExiting...")
