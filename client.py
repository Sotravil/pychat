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
        message = input("[Global] > ")
        if message == "/menu":
            break
        response = send_request(client, f"GLOBAL:{message}")
        if response:
            print(response)

def private_chat(client):
    """Private chat functionality."""
    recipient = input("Enter the username of the recipient: ")
    print(f"Starting private chat with {recipient}. Type your message or '/end' to return to the main menu.")
    while True:
        message = input("[Private] > ")
        if message == "/end":
            break
        response = send_request(client, f"PRIVATE:{recipient}:{message}")
        if response:
            print(response)

def group_chat(client):
    """Group chat functionality."""
    group = input("Enter the group name: ")
    response = send_request(client, f"JOIN_GROUP:{group}")
    if response:
        print(response)
    print(f"Joined group '{group}'. Type your message or '/leave' to leave the group.")
    while True:
        message = input("[Group] > ")
        if message == "/leave":
            send_request(client, f"LEAVE_GROUP:{group}")
            break
        response = send_request(client, f"GROUP:{group}:{message}")
        if response:
            print(response)

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
        command = input("[Profile] > ")
        if command == "/menu":
            break
        elif command == "/view":
            response = send_request(client, "VIEW_PROFILE")
            if response:
                print("Your Profile:")
                print(response)
        elif command.startswith("/edit"):
            field = input("Enter the field you want to edit (e.g., 'username', 'bio'): ")
            value = input(f"Enter the new value for {field}: ")
            response = send_request(client, f"EDIT_PROFILE:{field}:{value}")
            if response:
                print(response)
        else:
            print("Invalid command. Use '/view', '/edit', or '/menu'.")

def help_center(client):
    """Access the help center."""
    while True:
        page = input("Enter help page number (or '/menu' to return): ")
        if page == "/menu":
            break
        response = send_request(client, f"HELP:{page}")
        if response:
            print(response)

def main_menu(client):
    """Display the main menu and handle user actions."""
    while True:
        print("\nMain Menu:")
        print("1. Global Chat")
        print("2. Private Chat")
        print("3. Group Chat")
        print("4. Notifications")
        print("5. Manage Profile")
        print("6. Help Center")
        print("7. Logout")
        choice = input("Select an option (1-7): ")

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
            help_center(client)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select an option between 1-7.")

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
