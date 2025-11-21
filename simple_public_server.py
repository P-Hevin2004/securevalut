#!/usr/bin/env python3
"""
Simple script to start Django server with public access
"""
import subprocess
import sys
import os

def main():
    print("🌐 Starting File Share Server with Public Access...")
    print("=" * 60)
    print("📋 Instructions for sharing files with other people:")
    print("=" * 60)
    print("1. 🌍 Get your public IP address:")
    print("   - Visit: https://whatismyipaddress.com")
    print("   - Note down your public IP")
    print()
    print("2. 🔧 Configure your router (if needed):")
    print("   - Open port 8000 in your router settings")
    print("   - Forward port 8000 to your computer's IP")
    print()
    print("3. 📱 Share files:")
    print("   - Upload files to your system")
    print("   - Share QR codes or links with others")
    print("   - They can access via: http://YOUR_PUBLIC_IP:8000")
    print("=" * 60)
    print("🚀 Starting server...")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start Django server
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n✅ Server stopped!")

if __name__ == "__main__":
    main()
