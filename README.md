
---

# pychat - Console Chat Client

`pychat` is a console-based chat client for connecting to a Python chat server. It provides real-time communication in a global chatroom by default and offers features like user profiles, friend requests, and a notifications dashboard for managing interactions.

---

## **Features**
- **Global Chatroom**:
  - Default chatroom where all connected users can send and receive messages.
- **User Profiles**:
  - View other users' profiles and manage your own.
- **Friend Requests**:
  - Add other users as friends and accept/decline friend requests.
- **Notifications**:
  - A dashboard section to view and manage friend requests or system messages.
- **Inbox**:
  - Send and receive private messages with your friends.

---

## **Setup**

### **Requirements**
- Python 3.x
- A running `pychat` server exposed via Ngrok or localhost.

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pychat.git
   cd pychat
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the server details in `config.json`:
   ```json
   {
       "server_host": "a3cb-12-198-115-229.ngrok-free.app",
       "server_port": 5000
   }
   ```

4. Run the client:
   ```bash
   python client.py
   ```

---

## **Usage**

### **Main Menu**
After logging in, you’ll see the following options:

```plaintext
Welcome to pychat!
1. Global Chat (default)
2. Check Notifications
3. View Inbox
4. Manage Profile
5. Logout
```

#### **Option 1: Global Chat**
- By default, you’re placed in the global chatroom.
- Type messages to broadcast to all users in the room.
- Use `/menu` to return to the main menu.

#### **Option 2: Check Notifications**
- Displays a list of pending friend requests and other system messages.
- Example notification:
  ```plaintext
  Friend Request:
  user213 wants to add you as a friend and start chatting with you:
  Accept (Y) / Decline (N) / Ignore (Enter)
  ```
- Accept or decline requests directly in the notifications menu.

#### **Option 3: View Inbox**
- Shows private messages from friends.
- Allows you to respond to messages directly.

#### **Option 4: Manage Profile**
- View your profile details.
- Commands:
  - `/edit` - Update your profile (e.g., username, bio).
  - `/view <username>` - View another user's profile.
  - `/add <username>` - Send a friend request to another user.

#### **Option 5: Logout**
- Disconnects you from the server.

---

## **Commands**
You can use the following commands in the global chat or other sections:

- `/menu` - Return to the main menu.
- `/view <username>` - View another user's profile.
- `/add <username>` - Send a friend request.
- `/inbox` - Open your inbox directly.
- `/help` - Display available commands.

---

## **Notifications Section**
When you receive a friend request or system notification, a red marker appears in the notifications section:
```plaintext
Notifications (1)
```

You can view notifications, accept or decline friend requests, or mark them as read. Example workflow:
```plaintext
Friend Request:
user213 wants to add you as a friend and start chatting with you:
Accept (Y) / Decline (N) / Ignore (Enter)
```

---

## **Friend Request Workflow**

1. **Send a Friend Request**:
   - Use `/add <username>` to send a request.
   - The recipient sees a notification in their dashboard.

2. **Respond to Friend Requests**:
   - Go to the notifications menu and respond:
     - Accept: Adds the user to your friends list and allows private messaging.
     - Decline: Removes the request.
     - Ignore: Leaves the request pending.

---

## **Inbox**
Once users are friends, they can send private messages:
1. Use `/inbox` to open your inbox.
2. Select a friend to chat with.
3. Type messages directly.

Example:
```plaintext
Inbox:
1. user213
2. user345
Select a user to chat with: 1
```

---

## **Example Interaction**
### **Scenario 1: Global Chat**
```plaintext
> Hello, everyone!
Server: Welcome, user123!
> /add user456
Server: Friend request sent to user456.
```

### **Scenario 2: Notifications**
```plaintext
Notifications (1):
user456 wants to add you as a friend and start chatting with you:
Accept (Y) / Decline (N) / Ignore (Enter)
> Y
Server: You are now friends with user456.
```

---

## **Logout**
To log out, select option 5 from the main menu or type `/logout` in the chat. This disconnects you from the server.

---

