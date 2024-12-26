import os
import sys
import json
import time
import requests
import subprocess

import socketio  # python-socketio client library

# Replace with your server's address and port
SERVER_URL = "http://127.0.0.1:5000"

# The local version of the client—could be read from a local file version.json
LOCAL_CLIENT_VERSION = "1.0.0"

# A minimal directory path for the Git repository. In practice, ensure it points
# to your local 'pychat' repo clone.
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

# Create a SocketIO client instance
sio = socketio.Client()

##########################################################
# Socket.IO Event Handlers
##########################################################

@sio.event
def connect():
    print("[CLIENT] Connected to server via SocketIO.")

@sio.event
def connect_error(data):
    print("[CLIENT] Connection failed!", data)

@sio.event
def disconnect():
    print("[CLIENT] Disconnected from server.")

@sio.on('message')
def on_message(data):
    """Handle broadcast messages from the server."""
    print(f"[CLIENT] Broadcast message from server: {data}")

@sio.on('server_version_updated')
def on_server_version_updated(data):
    """
    Server notifies that a new version is available.
    data might look like: {'version': '1.0.1'}
    """
    new_version = data.get("version", "unknown")
    print(f"[CLIENT] Server version changed to {new_version}!")
    # Compare local version to new server version
    # In your current logic, any difference means an update is needed.
    if LOCAL_CLIENT_VERSION != new_version:
        print("[CLIENT] Your client might be out of date!")
        # Optionally ask user if they want to run an update
        choice = input("A new server version is available. Update client repo? (Y/N): ")
        if choice.lower() == "y":
            update_client_repo()

##########################################################
# Automated Update Logic
##########################################################

def update_client_repo():
    """
    Automate a git pull to update this local repository.
    """
    print("[CLIENT] Attempting to pull latest changes from GitHub...")
    try:
        # Ensure we're in the correct repository directory
        os.chdir(REPO_PATH)

        # Run a 'git pull' command
        result = subprocess.run(["git", "pull", "origin", "main"],
                                text=True, capture_output=True, check=False)
        if result.returncode == 0:
            print("[CLIENT] Pull successful. The client code is now updated!")
            print("[CLIENT] Please restart the client to load new changes (if code changed).")
        else:
            print("[CLIENT] Pull failed. See output below:")
            print(result.stderr)
    except Exception as e:
        print("[CLIENT] Error running git pull:", e)

##########################################################
# HTTP Version Check
##########################################################

def check_version_http():
    """
    Call /version-check endpoint via HTTP to see if local_version differs.
    """
    print(f"[CLIENT] Checking version via HTTP. Local: {LOCAL_CLIENT_VERSION}")
    payload = {"client_version": LOCAL_CLIENT_VERSION}
    try:
        resp = requests.post(f"{SERVER_URL}/version-check", json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            server_ver = data.get("current_server_version", "unknown")
            if data.get("needs_update", False):
                print(f"[CLIENT] The server has version: {server_ver}, which differs from local {LOCAL_CLIENT_VERSION}")
                # Prompt to update
                choice = input("Update client repo? (Y/N): ")
                if choice.lower() == "y":
                    update_client_repo()
            else:
                print("[CLIENT] No update needed. You're in sync with the server.")
        else:
            print("[CLIENT] /version-check failed with status:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("[CLIENT] Error calling /version-check:", e)

##########################################################
# Main Program Flow
##########################################################

def main_menu():
    while True:
        print("\n--- PyChat Client Menu ---")
        print("1. Connect to SocketIO server")
        print("2. Check version via HTTP")
        print("3. Update client repo now (manual git pull)")
        print("4. Disconnect from SocketIO server")
        print("5. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            # Connect if not already connected
            if not sio.connected:
                try:
                    sio.connect(SERVER_URL, wait_timeout=5)
                except Exception as e:
                    print("[CLIENT] Failed to connect via SocketIO:", e)
            else:
                print("[CLIENT] Already connected.")
        elif choice == "2":
            check_version_http()
        elif choice == "3":
            update_client_repo()
        elif choice == "4":
            if sio.connected:
                sio.disconnect()
            else:
                print("[CLIENT] Not currently connected.")
        elif choice == "5":
            if sio.connected:
                sio.disconnect()
            print("[CLIENT] Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
