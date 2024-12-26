"""
client.py - PyChat Client with Automatic Dependency Installation

Usage:
  python client.py
"""

import sys
import subprocess
import os

###############################################################################
# Auto-Install Dependencies
###############################################################################

def ensure_dependencies_installed():
    """
    Attempt to import required packages, and if any are missing,
    install them using pip at runtime.
    """
    required_packages = {
        # If you need Flask-SocketIO or additional dependencies, add them here:
        "flask": "Flask==2.2.3",
        "requests": "requests==2.31.0",
        "socketio": "python-socketio==5.6.0"
    }

    # For each library we need, try importing; if failing, pip install it.
    for import_name, pkg_version in required_packages.items():
        try:
            __import__(import_name)  # Attempt to import
        except ImportError:
            print(f"[CLIENT] Missing package '{import_name}'. Installing {pkg_version}...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg_version],
                check=False
            )

# Immediately ensure dependencies are installed before continuing
ensure_dependencies_installed()

###############################################################################
# Now that dependencies are installed, we can safely import them
###############################################################################
import requests
import socketio

###############################################################################
# Configuration
###############################################################################

SERVER_URL = "https://af71-12-198-115-229.ngrok-free.app"  # Replace with your server's URL
LOCAL_CLIENT_VERSION = "1.0.0"  # Example version; adjust or load from file
REPO_PATH = os.path.dirname(os.path.abspath(__file__))  # Directory for 'git pull'

sio = socketio.Client()

###############################################################################
# Socket.IO Events
###############################################################################

@sio.event
def connect():
    print("[CLIENT] Connected to server via Socket.IO.")

@sio.event
def connect_error(data):
    print("[CLIENT] Socket.IO connection failed:", data)

@sio.event
def disconnect():
    print("[CLIENT] Disconnected from the server.")

@sio.on("message")
def on_message(data):
    """Handle broadcast messages from the server."""
    print("[CLIENT] Broadcast from server:", data)

@sio.on("server_version_updated")
def on_server_version_updated(data):
    """
    Triggered when the server side has a new version.
    data might look like: {'version': '1.0.2'}
    """
    new_version = data.get("version", "unknown")
    print(f"[CLIENT] Server indicates a new version: {new_version}")

    if LOCAL_CLIENT_VERSION != new_version:
        print("[CLIENT] Your local client version is out of date.")
        choice = input("Update client code with 'git pull'? (y/n): ").strip().lower()
        if choice == "y":
            update_client_repo()

###############################################################################
# Update / Git Pull
###############################################################################

def update_client_repo():
    """
    Run 'git pull' to update local repository. Make sure you have credentials set
    if your repo is private.
    """
    print("[CLIENT] Pulling latest changes from the repository...")
    try:
        os.chdir(REPO_PATH)
        result = subprocess.run(["git", "pull", "origin", "main"],
                                text=True, capture_output=True)
        if result.returncode == 0:
            print("[CLIENT] Successfully pulled updates! Restart if code changed.")
        else:
            print("[CLIENT] Git pull failed. Output:")
            print(result.stderr)
    except Exception as e:
        print("[CLIENT] Error running git pull:", e)

###############################################################################
# HTTP Version Check
###############################################################################

def check_version_http():
    """
    Call /version-check with the local client version to see if we need an update.
    """
    print(f"[CLIENT] Checking version via HTTP. Local: {LOCAL_CLIENT_VERSION}")
    payload = {"client_version": LOCAL_CLIENT_VERSION}
    try:
        resp = requests.post(f"{SERVER_URL}/version-check", json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            server_ver = data.get("current_server_version", "unknown")
            needs_update = data.get("needs_update", False)
            if needs_update:
                print(f"[CLIENT] Server version differs: {server_ver}. Local is {LOCAL_CLIENT_VERSION}.")
                choice = input("Pull latest code from the repo? (y/n): ").strip().lower()
                if choice == 'y':
                    update_client_repo()
            else:
                print("[CLIENT] No update needed. We match the server version.")
        else:
            print("[CLIENT] /version-check returned status:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("[CLIENT] Error calling /version-check:", e)

###############################################################################
# Menu / Main Flow
###############################################################################

def main_menu():
    while True:
        print("\n=== PyChat Client Menu ===")
        print("1. Connect to server (SocketIO)")
        print("2. Check version via HTTP (/version-check)")
        print("3. Pull latest code now (manual git pull)")
        print("4. Disconnect from server")
        print("5. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            connect_socketio()
        elif choice == "2":
            check_version_http()
        elif choice == "3":
            update_client_repo()
        elif choice == "4":
            disconnect_socketio()
        elif choice == "5":
            print("[CLIENT] Exiting client...")
            if sio.connected:
                sio.disconnect()
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def connect_socketio():
    """Connect to the server via Socket.IO if not already connected."""
    if not sio.connected:
        try:
            print("[CLIENT] Connecting via Socket.IO...")
            # 'wait_timeout' in seconds to avoid indefinite hangs
            sio.connect(SERVER_URL, wait_timeout=5)
        except Exception as e:
            print("[CLIENT] Socket.IO connection failed:", e)
    else:
        print("[CLIENT] Already connected.")

def disconnect_socketio():
    """Disconnect from the server if connected."""
    if sio.connected:
        sio.disconnect()
        print("[CLIENT] Disconnected.")
    else:
        print("[CLIENT] Not currently connected to server.")

###############################################################################
# Main Entry
###############################################################################

if __name__ == "__main__":
    print("[CLIENT] Auto-installing dependencies if needed...")
    # We already called ensure_dependencies_installed() at the top,
    # but if you want to double-check, call it again here if needed.

    main_menu()
