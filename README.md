# PingPoke – Real-time VPN & Server Latency Monitor

A lightweight Python3 script designed to monitor network latency and VPN connectivity in real time. It pings multiple servers, displays ping times, packet drops, and automatically checks whether you are connected to a VPN. The output is presented in a clean, color-coded table that refreshes every few seconds, giving you a live snapshot of your network health.

## 🚀 Features

- **Real-time monitoring**: Continuously pings multiple servers with configurable intervals
- **Packet loss tracking**: Displays packet loss percentages for quick troubleshooting
- **VPN status detection**: Automatically detects VPN connection status via system network interfaces
- **Geographic information**: Shows server locations using IP geolocation
- **Color-coded output**: Easy-to-read status indicators
- **Live updates**: Refreshes in place without cluttering your terminal

## 🎨 Color Coding

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Good ping (< 100ms) / VPN connected |
| 🟡 **Yellow** | Moderate latency (100-200ms) |
| 🔴 **Red** | High latency (> 200ms) / VPN disconnected |
| ⚪ **Gray** | Timeout or unreachable host |

## 📋 Requirements

- Python 3.6+
- Internet connection
- macOS/Linux (for VPN interface detection)

## 🛠️ Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   python3 -m venv venv3
   source venv3/bin/activate
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the script:
```bash
python3 poker.py
```

Press `Ctrl+C` to exit.

## ⚙️ Configuration

Edit the `poker.py` file to customize:

- **Servers**: Add/remove servers in the `servers` dictionary
- **Ping interval**: Change the `interval` variable (default: 2 seconds)
- **VPN interface**: Modify the `interface_name` parameter in `vpn_connected()` function (default: "utun4")

## 📊 Sample Output

```
System Time: 2024-01-15 14:30:25
VPN Status: CONNECTED

Server                        Location/Region          Ping/ms      Packet Drops    
-------------------------------------------------------------------------------------           
speedtest.ph                  Manila, PH               89.67 ms     0%              
speedtest.com.sg              Singapore, SG            156.78 ms    0%              
speedtest.london.linode.com   London, GB               118.90 ms    0%              
```

## 🎯 Use Cases

- **Network administrators**: Monitor server connectivity and performance
- **Remote workers**: Check VPN status and connection quality
- **Gamers**: Monitor latency to game servers
- **Developers**: Test connectivity to various endpoints
- **Anyone**: Quick network health checks

## 📝 Notes

- The script uses `ifconfig` to detect VPN interfaces (macOS/Linux)
- IP geolocation is provided by ipinfo.io
- Default VPN interface is set to "utun4" (common for macOS VPNs)
- Timeout is set to 2 seconds for ping operations

## 👨‍💻 Author

**Badz Asterisk**

---
