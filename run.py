#!/usr/bin/env python3
# run.py
# Simple launcher for micPlan

import subprocess
import sys
import os
import socket

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except OSError:
            return True

def find_available_port(start_port=8502):
    """Find an available port starting from start_port"""
    port = start_port
    while is_port_in_use(port):
        port += 1
        if port > start_port + 10:  # Don't try more than 10 ports
            raise RuntimeError("No available ports found")
    return port

def main():
    """Launch micPlan using streamlit"""
    try:
        print("🚀 Starting micPlan...")
        
        # Find available port
        port = find_available_port()
        if port != 8502:
            print(f"⚠️  Port 8502 is in use, using port {port} instead")
        
        print(f"📱 Opening in your default browser on port {port}...")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(port),
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 micPlan stopped by user")
    except Exception as e:
        print(f"❌ Error starting micPlan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
