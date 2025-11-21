#!/usr/bin/env python3
"""
Test script to verify server accessibility
"""
import requests
import time

def test_server():
    print("🔍 Testing file sharing server connection...")
    print("=" * 50)
    
    # Your computer's IP address
    ip_address = "192.168.0.115"
    port = "8000"
    url = f"http://{ip_address}:{port}"
    
    print(f"🌐 Server URL: {url}")
    print(f"📱 Phone URL: {url}")
    print()
    
    try:
        print("⏳ Testing connection...")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible!")
            print("📱 Your phone should be able to access it now!")
            print()
            print("📋 Instructions for your phone:")
            print(f"   1. Open your phone's browser")
            print(f"   2. Go to: {url}")
            print(f"   3. You should see the file sharing homepage")
            print()
            print("📱 For QR codes:")
            print("   1. Upload a file on your computer")
            print("   2. Click 'QR Code' button")
            print("   3. Scan the QR code with your phone")
            print("   4. It should work now!")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("💡 Make sure:")
        print("   - Server is running (python manage.py runserver 0.0.0.0:8000)")
        print("   - Phone is on the same WiFi network")
        print("   - Firewall is not blocking the connection")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_server()
