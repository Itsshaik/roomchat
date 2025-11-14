# SecureChat - Encrypted Messaging Application

## Overview
SecureChat is a Django-based encrypted messaging application with password-protected chat rooms and real-time communication using WebSockets.

**Current State:** Fully functional MVP with all core features implemented
**Last Updated:** November 14, 2025

## Key Features
- User authentication (register, login, logout)
- Password-protected chat rooms
- Real-time messaging using Django Channels and WebSockets
- End-to-end message encryption using Fernet symmetric encryption
- Modern, professional UI with Tailwind CSS
- Encrypted message storage in SQLite database

## Project Architecture

### Technology Stack
**Backend:**
- Django 5.2.8
- Django Channels 4.3.1 (WebSocket support)
- Daphne 4.2.1 (ASGI server)
- Cryptography library (Fernet encryption)
- SQLite database

**Frontend:**
- Django Templates
- Tailwind CSS (via CDN)
- Vanilla JavaScript for WebSocket communication

### Project Structure
```
secureChat/
├── secureChat/          # Django project configuration
│   ├── settings.py      # Django settings with Channels config
│   ├── urls.py          # Main URL routing
│   └── asgi.py          # ASGI configuration for WebSockets
├── accounts/            # User authentication app
│   ├── views.py         # Login, register, logout views
│   ├── urls.py          # Authentication URLs
│   └── templates/       # Auth templates (login, register)
├── chat/                # Chat application
│   ├── models.py        # Room and Message models
│   ├── views.py         # Room management views
│   ├── consumers.py     # WebSocket consumer
│   ├── routing.py       # WebSocket URL routing
│   ├── encryption.py    # Message encryption utilities
│   ├── urls.py          # Chat URLs
│   └── templates/       # Chat templates (room list, join, chat)
└── db.sqlite3           # SQLite database

```

### Database Models
1. **Room**: Chat rooms with name, password, creator, and creation timestamp
2. **Message**: Encrypted messages with room, sender, encrypted content, and timestamp

### Security Features
- **Password Protection**: All chat rooms require password authentication
- **Hashed Passwords**: Room passwords are hashed using Django's make_password/check_password
- **WebSocket Authentication**: WebSocket connections verify authenticated users and session-based room access
- **Server-side Identity**: Username is enforced server-side (self.scope['user']) to prevent spoofing
- **Message Encryption**: Fernet symmetric encryption for all messages stored in database
- **Session-based Access Control**: Room access tracked in user sessions
- **Encrypted Key Storage**: Encryption key stored in .encryption_key file (excluded from git)

### Encryption
Messages are encrypted using the cryptography library's Fernet symmetric encryption:
- Encryption key is generated once and stored in `.encryption_key`
- All messages are encrypted before storing in the database
- Messages are decrypted on retrieval for authorized users

## Recent Changes
- **Nov 14, 2025**: Initial project setup with all core features
  - Created Django project with Channels support
  - Implemented user authentication system
  - Built password-protected room system with hashed passwords
  - Added real-time WebSocket messaging with authentication
  - Integrated Fernet encryption for messages
  - Designed modern UI with Tailwind CSS
  - Fixed critical security issues:
    * WebSocket authentication and room access verification
    * Hashed room passwords (Django make_password/check_password)
    * Server-side username enforcement (no client spoofing)

## How to Use

### For Users
1. **Register**: Create an account with username and password
2. **Login**: Sign in with your credentials
3. **Create Room**: Enter room name and set a password
4. **Join Room**: Click on a room and enter its password
5. **Chat**: Send encrypted messages in real-time

### Admin Panel
- **URL**: `/admin/`
- **Features**:
  - View all rooms and messages
  - See encryption status (🔐 ENCRYPTED indicator)
  - Decrypt and view message content
  - Room password protection status (🔒 Protected)
  - Search and filter messages by room or user

### For Developers
- **Run Server**: Workflow "SecureChat Server" runs: `daphne -b 0.0.0.0 -p 5000 secureChat.asgi:application`
- **Redis Server**: Workflow "Redis Server" runs: `redis-server --port 6000`
- **Migrations**: `python manage.py makemigrations && python manage.py migrate`
- **Create Superuser**: `python manage.py createsuperuser`

## Workflow Configuration
1. **Redis Server**
   - **Command**: `redis-server --port 6000`
   - **Port**: 6000
   - **Type**: Console (background service)
   
2. **SecureChat Server**
   - **Command**: `daphne -b 0.0.0.0 -p 5000 secureChat.asgi:application`
   - **Port**: 5000
   - **Type**: Webview (accessible via browser)

## Environment
- Python 3.11
- Django 5.2.8
- Redis 7.2.10 (running on port 6000)
- Channel layers: Redis (production-ready)

## User Preferences
None specified yet.
