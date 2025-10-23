# Snapchat Clone - API Reference

Quick reference guide for all API endpoints.

---

## 🔐 Authentication Endpoints

### Signup
```
POST /signup/
Content-Type: application/x-www-form-urlencoded

Fields:
- username: string
- email: string
- password: string

Response: Redirect to login
```

### Login
```
POST /login/
Content-Type: application/x-www-form-urlencoded

Fields:
- username: string
- password: string

Response: Redirect to home
```

### Logout
```
POST /logout/

Response: Redirect to login
```

---

## 📸 Snap Endpoints

### Send Snap
```
POST /snap/send/
Content-Type: multipart/form-data
Auth: Required

Fields:
- receiver: string (username)
- media: file (image or video, max 10MB)
- caption: string (optional, max 200 chars)
- duration: integer (5, 10, or 15 seconds)

Response:
{
  "success": true,
  "snap_id": 123,
  "message": "Snap sent to username"
}
```

### Get Received Snaps
```
GET /snap/received/
Auth: Required

Response:
[
  {
    "id": 123,
    "sender": "username",
    "media_type": "image",
    "caption": "Hello!",
    "sent_at": "Oct 22, 2025 03:30 PM",
    "is_opened": false
  }
]
```

### View Snap
```
GET /snap/view/<snap_id>/
Auth: Required

Response:
{
  "success": true,
  "media_url": "/media/snaps/2025/10/22/snap.jpg",
  "media_type": "image",
  "caption": "Hello!",
  "duration": 10,
  "sender": "username"
}

Error (410 if expired):
{
  "error": "Snap has expired"
}
```

### Get Sent Snaps
```
GET /snap/sent/
Auth: Required

Response:
[
  {
    "id": 123,
    "receiver": "username",
    "media_type": "video",
    "caption": "Check this out",
    "sent_at": "Oct 22, 2025 03:30 PM",
    "is_opened": true,
    "opened_at": "Oct 22, 2025 03:35 PM"
  }
]
```

---

## 📖 Story Endpoints

### Create Story
```
POST /story/create/
Content-Type: multipart/form-data
Auth: Required

Fields:
- media: file (image or video, max 10MB)
- caption: string (optional, max 200 chars)

Response:
{
  "success": true,
  "story_id": 456,
  "message": "Story created successfully",
  "expires_at": "Oct 23, 2025 03:30 PM"
}
```

### Get All Stories
```
GET /story/all/
Auth: Required

Response:
[
  {
    "id": 456,
    "creator": "username",
    "media_type": "image",
    "media_url": "/media/stories/2025/10/22/story.jpg",
    "caption": "My day",
    "created_at": "Oct 22, 2025 03:30 PM",
    "expires_at": "Oct 23, 2025 03:30 PM",
    "view_count": 25,
    "has_viewed": false,
    "is_own_story": false
  }
]
```

### View Story
```
POST /story/view/<story_id>/
Auth: Required

Response:
{
  "success": true,
  "media_url": "/media/stories/2025/10/22/story.jpg",
  "media_type": "image",
  "caption": "My day",
  "creator": "username",
  "created_at": "Oct 22, 2025 03:30 PM"
}

Error (410 if expired):
{
  "error": "Story has expired"
}
```

### Get Story Views
```
GET /story/views/<story_id>/
Auth: Required (must be story creator)

Response:
{
  "story_id": 456,
  "total_views": 25,
  "views": [
    {
      "viewer": "username",
      "viewed_at": "Oct 22, 2025 03:35 PM"
    }
  ]
}
```

### Delete Story
```
POST /story/delete/<story_id>/
DELETE /story/delete/<story_id>/
Auth: Required (must be story creator)

Response:
{
  "success": true,
  "message": "Story deleted"
}
```

---

## 💬 Message Endpoints

### Send Message
```
POST /message/send/
Content-Type: multipart/form-data
Auth: Required

Fields:
- receiver: string (username)
- content: string (required if no media)
- media: file (optional, image or video)

Response:
{
  "success": true,
  "message_id": 789,
  "sent_at": "Oct 22, 2025 03:30 PM"
}
```

### Get Conversations
```
GET /message/conversations/
Auth: Required

Response:
[
  {
    "username": "friend_username",
    "last_message": "Hey, how are you?",
    "last_message_time": "Oct 22, 2025 03:30 PM",
    "unread_count": 3
  }
]
```

### Get Message Thread
```
GET /message/thread/<username>/
Auth: Required

Response:
[
  {
    "id": 789,
    "sender": "friend_username",
    "receiver": "your_username",
    "content": "Hey, how are you?",
    "media_url": null,
    "sent_at": "Oct 22, 2025 03:30 PM",
    "is_read": true,
    "is_own_message": false
  }
]
```

### Mark Message as Read
```
POST /message/read/<message_id>/
Auth: Required

Response:
{
  "success": true
}
```

---

## 👥 Friend Endpoints

### Get Friends List
```
GET /friends/
Auth: Required

Response:
[
  {
    "username": "friend_username",
    "email": "friend@example.com",
    "last_interaction": "Oct 22, 2025 03:30 PM"
  }
]
```

### Send Friend Request
```
POST /send-request/
Content-Type: application/x-www-form-urlencoded
Auth: Required

Fields:
- receiver: string (username)

Response:
{
  "success": true,
  "message": "Friend request sent!"
}

Errors:
{
  "error": "User not found"
}
{
  "error": "Cannot send request to yourself"
}
{
  "error": "Request already sent"
}
```

### Get Pending Requests
```
GET /pending-requests/
Auth: Required

Response:
[
  {
    "sender": "username",
    "created_at": "Oct 22, 2025 03:30 PM"
  }
]
```

### Accept Friend Request
```
POST /accept-request/
Content-Type: application/x-www-form-urlencoded
Auth: Required

Fields:
- sender: string (username)

Response:
{
  "success": true,
  "message": "Friend request accepted!"
}

Errors:
{
  "error": "User not found"
}
{
  "error": "No pending request"
}
```

---

## 🏠 Page Endpoints

### Home Page
```
GET /
Auth: Required

Returns: home.html template with stories
```

### Messages Page
```
GET /messages.html
Auth: Required

Returns: messages.html template
```

### Snaps Page
```
GET /snaps.html
Auth: Required

Returns: snaps.html template
```

---

## 📝 Legacy Chat Endpoints

### Get Chats
```
GET /get-chats/
Auth: Required

Response:
[
  {
    "name": "Friend Name",
    "emoji": "👨‍💼",
    "time": "Oct 22, 2025 03:30 PM"
  }
]
```

### Add Chat
```
POST /add-chat/
Auth: Required

Response:
{
  "success": true,
  "chat": {
    "name": "Random Name",
    "emoji": "👩‍💻",
    "time": "Oct 22, 2025 03:30 PM"
  }
}
```

---

## 🔧 Error Responses

### Common Error Codes

**400 Bad Request**
```json
{
  "error": "Description of what went wrong"
}
```

**403 Forbidden**
```json
{
  "error": "Login required"
}
```

**404 Not Found**
```json
{
  "error": "User not found"
}
```

**405 Method Not Allowed**
```json
{
  "error": "Invalid request method"
}
```

**410 Gone** (Expired content)
```json
{
  "error": "Snap has expired"
}
```

---

## 📊 File Upload Limits

- **Max File Size:** 10MB
- **Allowed Image Types:** JPEG, PNG, GIF, WebP
- **Allowed Video Types:** MP4, QuickTime, AVI

---

## 🔒 Authentication

All endpoints marked "Auth: Required" need:
- User must be logged in via Django session
- Session cookie automatically included by browser

For API testing:
1. Login via `/login/` endpoint
2. Session cookie will be set
3. Use that session for subsequent requests

---

## 🧪 Testing with cURL

### Example: Send a Snap
```bash
curl -X POST http://localhost:8000/snap/send/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -F "receiver=friend_username" \
  -F "media=@/path/to/photo.jpg" \
  -F "caption=Hello!" \
  -F "duration=10"
```

### Example: Get Stories
```bash
curl -X GET http://localhost:8000/story/all/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

---

## 📱 JavaScript Integration

All API endpoints return JSON and can be called from JavaScript:

```javascript
// Example: Get stories
async function getStories() {
  const response = await fetch('/story/all/');
  const stories = await response.json();
  return stories;
}

// Example: Send message
async function sendMessage(receiver, content) {
  const formData = new FormData();
  formData.append('receiver', receiver);
  formData.append('content', content);
  
  const response = await fetch('/message/send/', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}
```

---

## 🎯 Best Practices

1. **Always check response status codes**
2. **Handle errors gracefully**
3. **Use FormData for file uploads**
4. **Implement loading states in UI**
5. **Cache data when appropriate**
6. **Implement retry logic for failed requests**
7. **Validate input before sending**

---

**Version:** 2.0  
**Last Updated:** October 22, 2025

