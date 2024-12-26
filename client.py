import requests

# Update with your actual ngrok URL
BASE_URL = "https://af71-12-198-115-229.ngrok-free.app"

def get_server_version():
    """Fetch the server version from the server."""
    try:
        response = requests.get(f"{BASE_URL}/status")
        return response.json().get("version", "unknown")
    except Exception as e:
        print("Error fetching server version:", e)
        return "unknown"

def update_client():
    """Simulate an update process by notifying the user to pull the latest changes from the repository."""
    print("Checking for updates...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        server_version = response.json().get("version", "unknown")
        print(f"Server version: {server_version}")
        print("To update your client, please pull the latest changes from the repository.")
        print("Run: git pull origin main")
    except Exception as e:
        print("Error checking for updates:", e)

def main_menu():
    server_version = get_server_version()
    print(f"Welcome to the Terminal Menu Dashboard")
    print(f"Server Version: {server_version}")
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
