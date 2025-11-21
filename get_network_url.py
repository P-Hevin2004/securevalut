#!/usr/bin/env python3
"""
Script to get the network URL for QR code sharing
"""
import socket

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"🌐 Your server is accessible at:")
    print(f"   Computer: http://127.0.0.1:8000")
    print(f"   Phone/Other devices: http://{ip}:8000")
    print(f"\n📱 To use QR codes from your phone:")
    print(f"   1. Make sure your phone is on the same WiFi network")
    print(f"   2. Scan the QR code - it should work now!")
    print(f"   3. If it still doesn't work, manually visit: http://{ip}:8000")
