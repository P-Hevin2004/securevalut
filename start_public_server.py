#!/usr/bin/env python3
"""
Script to start the file sharing server with public access via ngrok
"""
import subprocess
import time
import sys
from pyngrok import ngrok
import threading

def start_django_server():
    """Start Django server in background"""
    print("🚀 Starting Django server...")
    subprocess.run([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("🌐 Setting up public file sharing server...")
    print("=" * 50)
    
    # Start Django server in background thread
    django_thread = threading.Thread(target=start_django_server, daemon=True)
    django_thread.start()
    
    # Wait for Django to start
    print("⏳ Waiting for Django server to start...")
    time.sleep(3)
    
    # Create ngrok tunnel
    print("🔗 Creating public tunnel...")
    try:
        # Create tunnel to localhost:8000
        public_url = ngrok.connect(8000)
        print(f"✅ Public URL created: {public_url}")
        print("=" * 50)
        print("🌍 Your file sharing system is now accessible worldwide!")
        print(f"📱 Share this URL with anyone: {public_url}")
        print("📱 QR codes will now work from any device, anywhere!")
        print("=" * 50)
        print("💡 Tips:")
        print("   - Upload files and share the QR codes")
        print("   - Anyone can scan and download files")
        print("   - No need to be on the same network")
        print("=" * 50)
        print("🛑 Press Ctrl+C to stop the server")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            ngrok.disconnect(public_url)
            print("✅ Server stopped successfully!")
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("💡 Make sure you have internet connection")
        print("💡 Try running: pip install pyngrok")

if __name__ == "__main__":
    main()
