#  Async TCP Chat Application (Python)

A lightweight real-time chat application built using Python’s `asyncio` and TCP sockets.
This project demonstrates how to handle multiple clients concurrently using asynchronous I/O — a core backend skill.

---

##  Features

*  Asynchronous server using `asyncio`
*  Multiple clients can connect simultaneously
*  Unique username enforcement
*  Real-time message broadcasting
*  Graceful client disconnect handling
*  Non-blocking I/O (no threads needed)

---

##  Project Structure

```
chat/
├── server.py   # Async TCP server
├── client.py   # CLI client
└── README.md
```

---

## ⚙️ Requirements

* Python 3.8+ (recommended: 3.10+)

Check your version:

```bash
python3 --version
```

---

## ▶ How to Run

### 1. Start the Server

```bash
python3 server.py
```

Expected output:

```
Server started on ('127.0.0.1', 12345)
```

---

### 2. Start a Client

Open a new terminal:

```bash
python3 client.py
```

Enter your username when prompted.

---

### 3. Start Multiple Clients

Run the client again in another terminal to simulate multiple users.

---

##  Example

```
Client 1:
Enter your username: terrich

Client 2:
Enter your username: harry

Chat:
terrich: hello
harry: hey bro
```

---

##  How It Works

###  Server (`server.py`)

* Uses `asyncio.start_server` to accept connections
* Maintains a dictionary of connected clients
* Handles:

  * username registration
  * message broadcasting
  * client cleanup on disconnect

###  Client (`client.py`)

* Connects to server via TCP (`127.0.0.1:12345`)
* Runs two async tasks:

  * receiving messages
  * sending user input

---

## ⚠️ Known Limitations

* ❌ No message persistence (in-memory only)
* ❌ No encryption (plain TCP)
* ❌ No authentication system
* ❌ Single server instance (no scaling)

---

##  Future Improvements

*  WebSocket support (real-world standard)
*  Chat history using a database (PostgreSQL / MongoDB)
*  Authentication (JWT / OAuth)
*  Chat rooms / channels
*  Redis Pub/Sub for scalability
*  Frontend UI (React / CLI enhancements)

---

##  Why This Project Matters

This project demonstrates:

* Async programming with `asyncio`
* Network communication fundamentals
* Handling concurrent clients
* Backend architecture basics

These are **core backend engineering skills** used in real systems like chat apps, multiplayer games, and live dashboards.

---

## 📌 Usage Notes

* Always start the server before connecting clients
* Each username must be unique
* Press `Ctrl+C` to exit client/server

---

##  Author

Built as a backend learning project to understand async systems and socket programming.

---

##  Contribute / Extend

Feel free to fork and improve:

* Add features
* Improve performance
* Build a UI on top

---

##  License

This project is open-source and free to use.







# Chat app written in python

### TODO

- [ ] Dockerize server
- [ ] Web-gui for client
- [ ] DB support for server with signup
