"""
client.py - PyChat Client with Automatic Dependency Installation, Styled Menus, and Clear Screen

Install or verify all necessary dependencies:
  - Flask==2.2.3
  - requests==2.31.0
  - python-socketio==5.6.0
  - colorama==0.4.6

Once dependencies are verified/installed, uses colorama for styled output and
clears the screen after each user choice.
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
        "flask": "Flask==2.2.3",
        "requests": "requests==2.31.0",
        "socketio": "python-socketio==5.6.0",
        "colorama": "colorama==0.4.6"
    }

    installed_any = False

    for import_name, pkg_version in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"[CLIENT] Missing package '{import_name}'. Installing {pkg_version}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg_version], check=False)
            installed_any = True

    if installed_any:
        clear_console()
        print("[CLIENT] Dependencies installed. Console cleared. Continuing...")

def clear_console():
    """Clear the console screen (Windows: cls, Linux/macOS: clear)."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Immediately ensure dependencies are installed
ensure_dependencies_installed()

###############################################################################
# Now import the packages we just installed
###############################################################################
import requests
import socketio
from colorama import init, Fore, Style

init(autoreset=True)

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
    print(Fore.GREEN + "[CLIENT] Connected to server via Socket.IO.")

@sio.event
def connect_error(data):
    print(Fore.RED + "[CLIENT] Socket.IO connection failed:", data)

@sio.event
def disconnect():
    print(Fore.YELLOW + "[CLIENT] Disconnected from the server.")

@sio.on("message")
def on_message(data):
    """Handle broadcast messages from the server."""
    print(Fore.MAGENTA + "[CLIENT] Broadcast from server:" + Style.RESET_ALL, data)

@sio.on("server_version_updated")
def on_server_version_updated(data):
    """
    Triggered when the server indicates a new version is available.
    e.g., data = {'version': '1.0.2'}
    """
    new_version = data.get("version", "unknown")
    print(Fore.CYAN + f"[CLIENT] Server indicates a new version: {new_version}")

    if LOCAL_CLIENT_VERSION != new_version:
        print(Fore.RED + "[CLIENT] Your local client version is out of date.")
        choice = input("Update client code with 'git pull'? (y/n): ").strip().lower()
        if choice == "y":
            update_client_repo()

###############################################################################
# Update / Git Pull
###############################################################################

def update_client_repo():
    """
    Run 'git pull' to update local repository. Assumes credentials are set if private.
    """
    print(Fore.YELLOW + "[CLIENT] Pulling latest changes from the repository...")
    try:
        os.chdir(REPO_PATH)
        result = subprocess.run(["git", "pull", "origin", "main"],
                                text=True, capture_output=True)
        if result.returncode == 0:
            print(Fore.GREEN + "[CLIENT] Successfully pulled updates! Restart if code changed.")
        else:
            print(Fore.RED + "[CLIENT] Git pull failed. Output:")
            print(result.stderr)
    except Exception as e:
        print(Fore.RED + "[CLIENT] Error running git pull:", e)

###############################################################################
# HTTP Version Check
###############################################################################

def check_version_http():
    """
    Call /version-check with the local client version to see if an update is needed.
    """
    print(Fore.CYAN + f"[CLIENT] Checking version via HTTP. Local: {LOCAL_CLIENT_VERSION}")
    payload = {"client_version": LOCAL_CLIENT_VERSION}
    try:
        resp = requests.post(f"{SERVER_URL}/version-check", json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            server_ver = data.get("current_server_version", "unknown")
            needs_update = data.get("needs_update", False)
            if needs_update:
                print(Fore.RED + f"[CLIENT] Server version differs: {server_ver}. Local is {LOCAL_CLIENT_VERSION}.")
                choice = input("Pull latest code from the repo? (y/n): ").strip().lower()
                if choice == 'y':
                    update_client_repo()
            else:
                print(Fore.GREEN + "[CLIENT] No update needed. We match the server version.")
        else:
            print(Fore.RED + "[CLIENT] /version-check returned status:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "[CLIENT] Error calling /version-check:", e)

###############################################################################
# Placeholder Login/Registration
###############################################################################

def user_login():
    """
    Placeholder for user login. Insert your actual logic here if needed.
    """
    print(Fore.YELLOW + "[CLIENT] Enter your username:")
    username = input("> ")
    print(Fore.YELLOW + "[CLIENT] Enter your password:")
    password = input("> ")
    print(Fore.BLUE + f"[CLIENT] Attempting login for username='{username}'... (not implemented)")

def user_register():
    """
    Placeholder for user registration. Insert your actual logic here if needed.
    """
    print(Fore.YELLOW + "[CLIENT] Enter your desired username:")
    username = input("> ")
    print(Fore.YELLOW + "[CLIENT] Enter your desired password:")
    password = input("> ")
    print(Fore.YELLOW + "[CLIENT] Enter your age:")
    age = input("> ")
    print(Fore.BLUE + f"[CLIENT] Attempting registration with username='{username}', age='{age}'... (not implemented)")

###############################################################################
# Menu / Main Flow
###############################################################################

def main_menu():
    while True:
        # Clear console each time we show the menu for a fresh UI
        clear_console()

        print(Fore.GREEN + Style.BRIGHT + f"=== PyChat Client Menu (Local v{LOCAL_CLIENT_VERSION}) ===" + Style.RESET_ALL)
        print(Fore.CYAN + "1." + Style.RESET_ALL + " Connect to server (SocketIO)")
        print(Fore.CYAN + "2." + Style.RESET_ALL + " Check version via HTTP (/version-check)")
        print(Fore.CYAN + "3." + Style.RESET_ALL + " Pull latest code now (manual git pull)")
        print(Fore.CYAN + "4." + Style.RESET_ALL + " Disconnect from server")
        print(Fore.CYAN + "5." + Style.RESET_ALL + " Log (Login placeholder)")
        print(Fore.CYAN + "6." + Style.RESET_ALL + " Reg (Register placeholder)")
        print(Fore.CYAN + "7." + Style.RESET_ALL + " Exit")

        choice = input(Fore.MAGENTA + "Select an option: " + Style.RESET_ALL).strip()

        if choice == "1":
            connect_socketio()
        elif choice == "2":
            check_version_http()
        elif choice == "3":
            update_client_repo()
        elif choice == "4":
            disconnect_socketio()
        elif choice == "5":
            user_login()
        elif choice == "6":
            user_register()
        elif choice == "7":
            print(Fore.YELLOW + "[CLIENT] Exiting client...")
            if sio.connected:
                sio.disconnect()
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice. Press Enter to continue...")
            input()

def connect_socketio():
    """Connect to the server via Socket.IO if not already connected."""
    if not sio.connected:
        try:
            print(Fore.MAGENTA + "[CLIENT] Connecting via SocketIO...")
            sio.connect(SERVER_URL, wait_timeout=5)
        except Exception as e:
            print(Fore.RED + "[CLIENT] Socket.IO connection failed:", e)
    else:
        print(Fore.RED + "[CLIENT] Already connected.")

def disconnect_socketio():
    """Disconnect from the server if connected."""
    if sio.connected:
        sio.disconnect()
        print(Fore.YELLOW + "[CLIENT] Disconnected.")
    else:
        print(Fore.RED + "[CLIENT] Not currently connected to server.")

###############################################################################
# Main Entry
###############################################################################

if __name__ == "__main__":
    print(Fore.GREEN + f"[CLIENT] Local client version is {LOCAL_CLIENT_VERSION}.")
    print(Fore.GREEN + "[CLIENT] All dependencies verified or installed.")
    input(Fore.MAGENTA + "Press Enter to proceed to the main menu...")
    main_menu()
