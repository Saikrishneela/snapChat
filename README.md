# 📸 Snapchat Clone

A full-featured Snapchat clone built with Django, featuring snaps, stories, real-time messaging, and friend management.

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-ready%20for%20testing-yellow.svg)

---

## ✨ Features

### 📸 Snaps
- Send disappearing photos/videos to friends
- Set viewing duration (5-15 seconds)
- Auto-expiration after viewing
- View tracking with timestamps
- Support for captions

### 📖 Stories
- Create 24-hour stories
- View friends' stories
- Track views and viewers
- Auto-expiration after 24 hours
- Support for images and videos

### 💬 Messages
- Real-time messaging interface
- Text and media messages
- Read receipts
- Conversation threads
- Unread message counters

### 👥 Friends
- Send/receive friend requests
- Friend management system
- View friends list
- Mutual friendship tracking

### 🔐 Authentication
- User signup and login
- Session management
- Google OAuth integration (configured)
- Email verification support

### 🎨 User Interface
- Modern, responsive design
- Mobile-friendly layouts
- Real-time updates
- Smooth animations
- WhatsApp-style messaging

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   cd /path/to/snapChat
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional but recommended)
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create media directories**
   ```bash
   mkdir -p media/snaps media/stories media/messages
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main app: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - Messages: http://localhost:8000/messages.html
   - Snaps: http://localhost:8000/snaps.html

---

## 📁 Project Structure

```
snapChat/
├── snapchat/                 # Main application
│   ├── models.py             # 8 database models
│   ├── views.py              # 30+ view functions
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin configurations
│   ├── templates/            # HTML templates
│   │   └── snapchat/
│   │       ├── home.html
│   │       ├── messages.html
│   │       ├── snaps.html
│   │       ├── login.html
│   │       └── signup.html
│   ├── static/               # Static files
│   │   └── snapchat/
│   │       ├── home.css
│   │       ├── style.css
│   │       ├── images/
│   │       └── script.js/
│   └── migrations/           # Database migrations
│
├── snapclone/                # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/                    # User uploads
│   ├── snaps/
│   ├── stories/
│   └── messages/
│
├── Documents/                # Documentation
│   ├── databaseBluePrint.md
│   ├── erDiagram.md
│   ├── persona.md
│   └── userStories.md
│
├── IMPLEMENTATION_GUIDE.md   # Detailed implementation guide
├── API_REFERENCE.md          # Complete API documentation
├── requirements.txt          # Python dependencies
├── env.example               # Environment variables template
├── manage.py                 # Django management script
└── db.sqlite3                # SQLite database
```

---

## 🎯 Core Models

| Model | Description |
|-------|-------------|
| **User** | Built-in Django user model |
| **Chat** | Legacy chat management |
| **FriendRequest** | Friend request system |
| **Friendship** | Mutual friendship tracking |
| **Message** | Direct messaging |
| **Snap** | Temporary photo/video sharing |
| **SnapView** | Snap view tracking |
| **Story** | 24-hour stories |
| **StoryView** | Story view tracking |

---

## 🔌 API Endpoints

### Authentication
- `POST /signup/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout

### Snaps
- `POST /snap/send/` - Send a snap
- `GET /snap/received/` - Get received snaps
- `GET /snap/sent/` - Get sent snaps
- `GET /snap/view/<id>/` - View a snap

### Stories
- `POST /story/create/` - Create a story
- `GET /story/all/` - Get all active stories
- `POST /story/view/<id>/` - View a story
- `GET /story/views/<id>/` - Get story views
- `POST /story/delete/<id>/` - Delete a story

### Messages
- `POST /message/send/` - Send a message
- `GET /message/conversations/` - Get conversation list
- `GET /message/thread/<username>/` - Get message thread
- `POST /message/read/<id>/` - Mark message as read

### Friends
- `POST /send-request/` - Send friend request
- `GET /pending-requests/` - Get pending requests
- `POST /accept-request/` - Accept friend request
- `GET /friends/` - Get friends list

📖 **[View Complete API Documentation](API_REFERENCE.md)**

---

## 🖥️ User Interface

### Home Page (`/`)
- View and create stories
- Chat list with friends
- Navigation to all features
- Real-time story updates

### Messages Page (`/messages.html`)
- WhatsApp-style interface
- Conversation list
- Real-time messaging
- Media attachments
- Read receipts

### Snaps Page (`/snaps.html`)
- Send snaps to friends
- View received snaps
- Track sent snaps
- Auto-expiring viewer

---

## 🛠️ Technology Stack

- **Backend:** Django 5.2.7
- **Database:** SQLite (development)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Authentication:** Django Auth + django-allauth
- **Media Storage:** Django file storage
- **Email:** SMTP (Gmail configured)

---

## 📚 Documentation

- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Comprehensive setup and feature guide
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[ER Diagram](Documents/erDiagram.md)** - Database schema
- **[User Stories](Documents/userStories.md)** - Feature requirements

---

## 🔒 Security

### ⚠️ Before Production

1. **Move secrets to environment variables**
   - Copy `env.example` to `.env`
   - Update all credentials
   - Never commit `.env` to version control

2. **Update settings.py**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   SECRET_KEY = os.getenv('SECRET_KEY')
   DEBUG = os.getenv('DEBUG', 'False') == 'True'
   ```

3. **Enable security features**
   - Remove `@csrf_exempt` decorators
   - Enable HTTPS redirects
   - Set secure cookie flags
   - Configure CORS properly

4. **Use production database**
   - PostgreSQL recommended
   - Configure connection pooling
   - Enable database backups

---

## 🧪 Testing

### Test User Flows

**Test Snaps:**
1. Create two user accounts
2. Add as friends
3. Send a snap from user A to user B
4. View snap as user B (note expiration)

**Test Stories:**
1. Create a story
2. View from another account
3. Check view count and viewers

**Test Messages:**
1. Send messages between users
2. Verify read receipts
3. Test media attachments

---

## 📊 Database Migrations

The project includes a migration file for all new models:
- `snapchat/migrations/0007_add_new_models.py`

To apply migrations:
```bash
python manage.py migrate
```

---

## 🎨 Customization

### Modify Time Zone
In `settings.py`:
```python
TIME_ZONE = 'Your/Timezone'  # e.g., 'America/New_York'
```

### Adjust File Upload Limits
In `settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20MB
```

### Change Story Duration
In `models.py` (Story model):
```python
self.expires_at = timezone.now() + timedelta(hours=48)  # 48 hours
```

---

## 🐛 Troubleshooting

### Migration Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Media Files 404
- Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured
- Check file permissions on media directories
- Verify DEBUG=True for development

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

---

## 🚧 Known Limitations

- No real-time WebSocket support (uses polling)
- No push notifications
- No AR filters/stickers for snaps
- No story replies/reactions
- No group messaging
- No end-to-end encryption

---

## 🔮 Future Enhancements

- [ ] Django Channels for WebSockets
- [ ] Push notifications (Firebase)
- [ ] AR filters and effects
- [ ] Story reactions and replies
- [ ] Group chat functionality
- [ ] Voice/video calling
- [ ] End-to-end encryption
- [ ] Story highlights
- [ ] Snap map feature
- [ ] Dark mode

---

## 👥 User Roles

### Admin Panel Access

- **Superuser:** Full access to all models
- **Staff Users:** Limited access based on permissions
- **Custom Permissions:**
  - View-only access for specific users
  - Model-specific permissions

---

## 📦 Dependencies

Main dependencies:
- Django 5.2.7
- django-allauth 65.12.1
- Pillow 11.0.0 (image processing)
- python-dotenv 1.0.0 (environment variables)
- pytz 2025.2 (timezone support)

See `requirements.txt` for complete list.

---

## 📝 License

This is a learning project. Feel free to use and modify as needed.

---

## 🤝 Contributing

This is an educational project, but improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 💡 Tips

1. **Use Chrome DevTools** for debugging JavaScript
2. **Check Django logs** for server-side errors
3. **Test with multiple users** using different browsers
4. **Monitor file uploads** in media directories
5. **Use Django Debug Toolbar** for performance analysis

---

## 📞 Support

For issues or questions:
1. Check the [Implementation Guide](IMPLEMENTATION_GUIDE.md)
2. Review the [API Reference](API_REFERENCE.md)
3. Inspect browser console for JS errors
4. Check Django server logs

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models Guide](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Django File Uploads](https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

## ✅ Implementation Status

- ✅ Database models (100%)
- ✅ API endpoints (100%)
- ✅ Admin configurations (100%)
- ✅ User interface (100%)
- ✅ JavaScript integration (100%)
- ⚠️ Migrations (pending Python/Django setup)
- ⚠️ Security improvements (recommended)
- ⚠️ Production deployment (not configured)

---

## 📈 Stats

- **8 Models** - Complete data schema
- **25+ Endpoints** - Full REST API
- **3 Page Templates** - Modern UI
- **1000+ Lines** of Python code
- **500+ Lines** of JavaScript
- **100% Feature** coverage from requirements

---

**Built with ❤️ using Django**

**Version:** 2.0  
**Last Updated:** October 22, 2025  
**Status:** Ready for Testing

---

*For detailed technical documentation, see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) and [API_REFERENCE.md](API_REFERENCE.md)*

