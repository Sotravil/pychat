# pychat - Console Chat Client

`pychat` is a console-based chat client designed to connect to a Python-powered chat server. It offers robust features such as global chat, private messaging, group chats, user profiles, and a notifications dashboard for managing interactions.

---

## **Features**

### **Global Chatroom**
- A default chatroom where all connected users can communicate in real time.

### **Private Messaging**
- Send and receive private messages with your friends.
- One-on-one conversations for personalized interactions.

### **Group Chats**
- Create and join group chats for topic-specific discussions.
- Manage group members and collaborate with like-minded users.

### **User Profiles**
- View and manage your profile information.
- Check other users’ profiles to learn more about them.

### **Friend Requests**
- Add users as friends and accept/decline friend requests.
- Build your network and chat privately with friends.

### **Notifications Dashboard**
- Manage friend requests and system notifications in one place.

### **Inbox**
- View and manage private and group conversations.
- Continue conversations with your friends or groups from the main menu.

---

## **Setup**

### **Requirements**
- Python 3.x
- A running `pychat` server (local or Ngrok-exposed).

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/Sotravil/pychat.git
   cd pychat
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the server details in `config.json`:
   ```json
   {
       "server_host": "[https://0bc4-12-198-115-229.ngrok-free.app]",
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
After logging in, you will see the following options:

```plaintext
Welcome to pychat!
1. Global Chat (default)
2. Private Chats
3. Group Chats
4. Check Notifications
5. View Inbox
6. Manage Profile
7. Logout
```

#### **Option 1: Global Chat**
- Communicate in the default global chatroom.
- Type messages to broadcast to all users.
- Use `/menu` to return to the main menu.

#### **Option 2: Private Chats**
- Start or continue private conversations with your friends.
- Commands:
  - `/chat <username>` - Open a private chat with a friend.
  - `/end` - End the private chat and return to the main menu.

Example:
```plaintext
Private Chat with user213:
> Hello!
user213: Hi, how are you?
> /end
```

#### **Option 3: Group Chats**
- Create or join group chats.
- Commands:
  - `/create <groupname>` - Create a new group chat.
  - `/join <groupname>` - Join an existing group chat.
  - `/leave` - Leave the current group chat.
  - `/members` - List all members in the group.

Example:
```plaintext
Group Chat: PythonEnthusiasts
> How do I optimize this code?
user345: Share your snippet, I can help!
> /members
Group Members:
- user123
- user345
- user678
> /leave
```

#### **Option 4: Check Notifications**
- View pending friend requests and system messages.
- Example notification:
  ```plaintext
  Friend Request:
  user213 wants to add you as a friend:
  Accept (Y) / Decline (N) / Ignore (Enter)
  ```

#### **Option 5: View Inbox**
- View recent private and group chats.
- Select a conversation to continue chatting.

Example:
```plaintext
Inbox:
1. Private Chat with user213
2. Group Chat: PythonEnthusiasts
Select a chat: 1
```

#### **Option 6: Manage Profile**
- View and edit your profile details.
- Commands:
  - `/edit` - Update your profile (e.g., username, bio).
  - `/view <username>` - View another user’s profile.
  - `/add <username>` - Send a friend request.

#### **Option 7: Logout**
- Disconnect from the server.

---

## **Commands**

### **General Commands**
- `/menu` - Return to the main menu.
- `/help` - Display available commands.

### **Global Chat**
- Type directly to broadcast messages.

### **Private Chats**
- `/chat <username>` - Open a private chat.
- `/end` - End the private chat.

### **Group Chats**
- `/create <groupname>` - Create a new group chat.
- `/join <groupname>` - Join an existing group.
- `/leave` - Leave the current group chat.
- `/members` - List group members.

### **Friend Requests**
- `/add <username>` - Send a friend request.

---

## **Example Interactions**

### **Scenario 1: Global Chat**
```plaintext
> Hello, everyone!
Server: Welcome, user123!
> /add user456
Server: Friend request sent to user456.
```

### **Scenario 2: Private Chat**
```plaintext
> /chat user456
Private Chat with user456:
> Hey, how’s it going?
user456: Good, thanks!
> /end
```

### **Scenario 3: Group Chat**
```plaintext
> /create PythonEnthusiasts
Server: Group chat 'PythonEnthusiasts' created.
> Hello, Python lovers!
user789: Hi! What's the topic today?
> /members
Group Members:
- user123
- user789
> /leave
```

### **Scenario 4: Notifications**
```plaintext
Notifications (1):
Friend Request:
user456 wants to add you as a friend:
Accept (Y) / Decline (N) / Ignore (Enter)
> Y
Server: You are now friends with user456.
```

---

## **Logout**
To log out, select option 7 from the main menu or type `/logout`. This disconnects you from the server.

---

Let us know if you encounter any issues or have suggestions to improve `pychat`!

