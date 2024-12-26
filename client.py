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

def main():
    print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")

    try:
        # Connect to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server!")

        # Receive welcome message
        print(client.recv(1024).decode('utf-8'))

        # Chat loop
        while True:
            message = input("> ")
            if message.lower() == "exit":
                print("Closing connection...")
                break
            client.send(message.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"Server: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
