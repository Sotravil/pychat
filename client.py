import requests

# Update with your actual ngrok URL
BASE_URL = "https://af71-12-198-115-229.ngrok-free.app"

def main_menu():
    print("Welcome to the Terminal Menu Dashboard")
    print("1. Check Welcome Message")
    print("2. Check Server Status")
    print("3. Exit")
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
        print("Exiting...")
        exit()
    else:
        print("Invalid choice. Try again.")
        main_menu()

if __name__ == "__main__":
    while True:
        main_menu()
