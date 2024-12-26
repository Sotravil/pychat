import os
import requests
import subprocess
from datetime import datetime

# Update with your actual ngrok URL
BASE_URL = "https://af71-12-198-115-229.ngrok-free.app"

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e.stderr}")
        return None

def get_local_version():
    """Fetch the local client version from version.json."""
    try:
        with open("version.json", "r") as f:
            version_data = json.load(f)
        return version_data.get("version", "unknown")
    except FileNotFoundError:
        print("version.json not found. Assuming version is 'unknown'.")
        return "unknown"

def get_server_version():
    """Fetch the server version from the server."""
    try:
        response = requests.get(f"{BASE_URL}/status")
        return response.json().get("version", "unknown")
    except Exception as e:
        print("Error fetching server version:", e)
        return "unknown"

def update_client():
    """Pull the latest changes from the GitHub repository and reload the client."""
    print("Checking for updates...")
    local_version = get_local_version()
    server_version = get_server_version()

    if local_version != server_version:
        print(f"New version available: {server_version}. Updating from version: {local_version}.")
        result = run_command(["git", "pull", "origin", "main"])
        if result:
            print("Update successful. Restarting...")
            clear_terminal()
            os.execv(__file__, ["python"] + sys.argv)
        else:
            print("Update failed. Please try again manually.")
    else:
        print("You are already running the latest version.")

def main_menu():
    server_version = get_server_version()
    print(f"Welcome to the Terminal Menu Dashboard (Server Version: {server_version})")
    print("1. Check Welcome Message")
    print("2. Check Server Status")
    print("3. Update Client")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        try:
            response = requests.get(f"{BASE_URL}/")
            print("Server Response:", response.json())
        except Exception as e:
            print("Error connecting to server:", e)

    elif choice == "2":
        try:
            response = requests.get(f"{BASE_URL}/status")
            print("Server Response:", response.json())
        except Exception as e:
            print("Error connecting to server:", e)

    elif choice == "3":
        update_client()

    elif choice == "4":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice. Try again.")
        main_menu()

if __name__ == "__main__":
    while True:
        main_menu()
