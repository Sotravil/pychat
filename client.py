import socket
import json

# Load configuration
CONFIG_FILE = "config.json"

try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Configuration file not found. Please create 'config.json' with the server details.")
    exit(1)

SERVER_HOST = config.get("server_host", "127.0.0.1")  # Default to localhost
SERVER_PORT = config.get("server_port", 5000)        # Default to port 5000

def send_request(client, command):
    """Send a command to the server and return the response."""
    try:
        client.send(command.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        return response
    except Exception as e:
        print(f"Error communicating with server: {e}")
        return None

def global_chat(client):
    """Global chat functionality."""
    print("Entering Global Chat. Type your message or '/menu' to return to the main menu.")
    while True:
        message = input("> ")
        if message == "/menu":
            break
        response = send_request(client, f"GLOBAL:{message}")
        if response:
            print(f"Server: {response}")

def private_chat(client):
    """Private chat functionality."""
    friend = input("Enter the username of the friend you want to chat with: ")
    print(f"Starting private chat with {friend}. Type your message or '/end' to return to the main menu.")
    while True:
        message = input("> ")
        if message == "/end":
            break
        response = send_request(client, f"PRIVATE:{friend}:{message}")
        if response:
            print(f"{friend}: {response}")

def group_chat(client):
    """Group chat functionality."""
    group = input("Enter the group name you want to join or create: ")
    response = send_request(client, f"JOIN_GROUP:{group}")
    if response:
        print(response)
    print(f"Entered group chat '{group}'. Type your message or '/leave' to leave the group.")
    while True:
        message = input("> ")
        if message == "/leave":
            send_request(client, f"LEAVE_GROUP:{group}")
            break
        response = send_request(client, f"GROUP:{group}:{message}")
        if response:
            print(f"Group {group}: {response}")

def notifications(client):
    """Check notifications."""
    print("Fetching notifications...")
    response = send_request(client, "NOTIFICATIONS")
    if response:
        print(response)
    else:
        print("No notifications at the moment.")

def manage_profile(client):
    """View and manage user profile."""
    print("Type '/view' to view your profile, '/edit' to update it, or '/menu' to return to the main menu.")
    while True:
        command = input("> ")
        if command == "/menu":
            break
        elif command == "/view":
            response = send_request(client, "VIEW_PROFILE")
            if response:
                print("Your Profile:")
                print(response)
        elif command == "/edit":
            field = input("Enter the field you want to edit (e.g., 'username', 'bio'): ")
            value = input(f"Enter the new value for {field}: ")
            response = send_request(client, f"EDIT_PROFILE:{field}:{value}")
            if response:
                print(response)
        else:
            print("Invalid command. Use '/view', '/edit', or '/menu'.")

def main_menu(client):
    """Display the main menu and handle user actions."""
    while True:
        print("\nMain Menu:")
        print("1. Global Chat")
        print("2. Private Chats")
        print("3. Group Chats")
        print("4. Check Notifications")
        print("5. Manage Profile")
        print("6. Logout")
        choice = input("Select an option (1-6): ")

        if choice == "1":
            global_chat(client)
        elif choice == "2":
            private_chat(client)
        elif choice == "3":
            group_chat(client)
        elif choice == "4":
            notifications(client)
        elif choice == "5":
            manage_profile(client)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select an option between 1-6.")

def main():
    print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")

    try:
        # Connect to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server!")

        # Receive welcome message
        print(client.recv(1024).decode('utf-8'))

        # Show the main menu
        main_menu(client)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
