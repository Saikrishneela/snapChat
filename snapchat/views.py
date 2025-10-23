from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.conf import settings
from .models import Chat, FriendRequest, Snap, SnapView, Story, StoryView, Message, Friendship
from django.utils import timezone
from django.utils.dateformat import format as date_format
from datetime import datetime, timedelta
import pytz, random, os
from django.core.files.storage import default_storage


#SIGNUP#

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
        return redirect('login')  
    return render(request, 'snapchat/signup.html')  

#LOGIN#

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'snapchat/login.html')

#LOGOUT#

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'snapchat/home.html')


@login_required
def messages_page(request):
    """Render messages page"""
    return render(request, 'snapchat/messages.html')


@login_required
def snaps_page(request):
    """Render snaps page"""
    return render(request, 'snapchat/snaps.html')

def send_welcome_email(request):
    if request.method == "POST":
        user_email = request.POST.get('email')
        subject = "Welcome to Snapchat Clone"
        message = "Hi! Thanks for signing up for Snapchat Clone."
        from_email = None  # uses DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        send_mail(subject, message, from_email, recipient_list,fail_silently=False)
        messages.success(request, f"Email sent to {user_email}!")

    return render(request, 'send_email.html')

#IST timezone

IST = pytz.timezone("Asia/Kolkata")

USER_EMOJIS = {
    "Santu Sir": "👨‍💼",
    "Akshay Tomar": "👩‍💻",
    "MaheshBabu": "🧑‍🚀",
    "Aravind": "👨‍🎨",
    "Hema": "👩‍🔬",
    "Navya": "🧑‍🍳",
    "Prajjwal": "🧑‍💻",
    "RajKishor": "🧑‍🚒",
    "Ravindra Singh": "👩‍⚕️",
    "Daniel": "🧑‍🔧"
}


@csrf_exempt
def add_chat(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=403)

        name = random.choice(list(USER_EMOJIS.keys()))
        emoji = USER_EMOJIS[name]
        chat = Chat.objects.create(user=request.user, name=name, emoji=emoji, time=timezone.now())

        ist_time = timezone.localtime(chat.time, IST)
        formatted_time = ist_time.strftime("%b %d, %Y %I:%M %p")

        return JsonResponse({
            "success": True,
            "chat": {"name": chat.name, "emoji": chat.emoji, "time": formatted_time}
        })
    return JsonResponse({"error": "Invalid request"}, status=400)



@login_required
def get_chats(request):
    chats = Chat.objects.filter(user=request.user).order_by('-time')
    data = []

    for chat in chats:
        ist_time = timezone.localtime(chat.time, IST)
        formatted_time = ist_time.strftime("%b %d, %Y %I:%M %p")
        data.append({"name": chat.name, "emoji": chat.emoji, "time": formatted_time})

    return JsonResponse(data, safe=False)

                        


@csrf_exempt
@login_required
def send_request(request):
    if request.method == "POST":
        receiver_name = request.POST.get("receiver").strip()
        try:
            receiver = User.objects.get(username=receiver_name)
            print("Receiver name:", receiver_name)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        if receiver == request.user:
            return JsonResponse({"error": "Cannot send request to yourself"}, status=400)

        existing = FriendRequest.objects.filter(sender=request.user, receiver=receiver).first()
        if existing:
            return JsonResponse({"error": "Request already sent"}, status=400)

        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return JsonResponse({"success": True, "message": "Friend request sent!"})

    return JsonResponse({"error": "Invalid request"}, status=400)



@csrf_exempt
@login_required
def accept_request(request):
    if request.method == "POST":
        sender_name = request.POST.get("sender")
        try:
            sender = User.objects.get(username=sender_name)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        fr = FriendRequest.objects.filter(sender=sender, receiver=request.user, is_accepted=False).first()
        if not fr:
            return JsonResponse({"error": "No pending request"}, status=404)

        fr.is_accepted = True
        fr.save()

        # Create friendship (ensure user1 < user2 to avoid duplicates)
        user1, user2 = (sender, request.user) if sender.id < request.user.id else (request.user, sender)
        Friendship.objects.get_or_create(user1=user1, user2=user2)

        # Add each other to chat list
        Chat.objects.create(user=request.user, name=sender.username, emoji="💬", time=timezone.now())
        Chat.objects.create(user=sender, name=request.user.username, emoji="💬", time=timezone.now())

        return JsonResponse({"success": True, "message": "Friend request accepted!"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
@login_required
def get_pending_requests(request):
    pending = FriendRequest.objects.filter(receiver=request.user, is_accepted=False)
    data = [{"sender": fr.sender.username, "created_at": fr.created_at.strftime("%b %d, %Y %I:%M %p")} for fr in pending]
    return JsonResponse(data, safe=False)


# ========================================
# HELPER FUNCTIONS
# ========================================

def get_friends(user):
    """Get all friends of a user"""
    friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
    friends = []
    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == user else friendship.user1
        friends.append(friend)
    return friends


def validate_media_file(file, allowed_types):
    """Validate uploaded media file"""
    if not file:
        return False, "No file provided"
    
    if file.content_type not in allowed_types:
        return False, f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
    
    if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        return False, f"File too large. Max size: {settings.FILE_UPLOAD_MAX_MEMORY_SIZE / 1048576}MB"
    
    return True, "Valid"


# ========================================
# SNAP VIEWS
# ========================================

@csrf_exempt
@login_required
def send_snap(request):
    """Send a snap to a friend"""
    if request.method == "POST":
        receiver_username = request.POST.get("receiver")
        caption = request.POST.get("caption", "")
        duration = int(request.POST.get("duration", 10))
        media_file = request.FILES.get("media")
        
        if not receiver_username:
            return JsonResponse({"error": "Receiver is required"}, status=400)
        
        if not media_file:
            return JsonResponse({"error": "Media file is required"}, status=400)
        
        # Validate file type
        allowed_types = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_VIDEO_TYPES
        is_valid, message = validate_media_file(media_file, allowed_types)
        if not is_valid:
            return JsonResponse({"error": message}, status=400)
        
        # Get receiver
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
        # Determine media type
        media_type = 'image' if media_file.content_type in settings.ALLOWED_IMAGE_TYPES else 'video'
        
        # Create snap
        snap = Snap.objects.create(
            sender=request.user,
            receiver=receiver,
            media_url=media_file,
            media_type=media_type,
            caption=caption,
            duration_seconds=duration
        )
        
        return JsonResponse({
            "success": True,
            "snap_id": snap.id,
            "message": f"Snap sent to {receiver.username}"
        })
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def get_received_snaps(request):
    """Get all unopened snaps received by user"""
    snaps = Snap.objects.filter(receiver=request.user, is_opened=False).order_by('-sent_at')
    
    data = []
    for snap in snaps:
        data.append({
            "id": snap.id,
            "sender": snap.sender.username,
            "media_type": snap.media_type,
            "caption": snap.caption,
            "sent_at": snap.sent_at.strftime("%b %d, %Y %I:%M %p"),
            "is_opened": snap.is_opened
        })
    
    return JsonResponse(data, safe=False)


@login_required
def view_snap(request, snap_id):
    """View a snap (marks it as opened and tracks view)"""
    snap = get_object_or_404(Snap, id=snap_id, receiver=request.user)
    
    if not snap.is_opened:
        snap.is_opened = True
        snap.opened_at = timezone.now()
        snap.save()
        
        # Track view
        SnapView.objects.get_or_create(snap=snap, viewer=request.user)
    
    # Check if snap is expired
    if snap.is_expired:
        return JsonResponse({"error": "Snap has expired"}, status=410)
    
    return JsonResponse({
        "success": True,
        "media_url": snap.media_url.url,
        "media_type": snap.media_type,
        "caption": snap.caption,
        "duration": snap.duration_seconds,
        "sender": snap.sender.username
    })


@login_required
def get_sent_snaps(request):
    """Get snaps sent by user with view status"""
    snaps = Snap.objects.filter(sender=request.user).order_by('-sent_at')[:20]
    
    data = []
    for snap in snaps:
        data.append({
            "id": snap.id,
            "receiver": snap.receiver.username,
            "media_type": snap.media_type,
            "caption": snap.caption,
            "sent_at": snap.sent_at.strftime("%b %d, %Y %I:%M %p"),
            "is_opened": snap.is_opened,
            "opened_at": snap.opened_at.strftime("%b %d, %Y %I:%M %p") if snap.opened_at else None
        })
    
    return JsonResponse(data, safe=False)


# ========================================
# STORY VIEWS
# ========================================

@csrf_exempt
@login_required
def create_story(request):
    """Create a new story"""
    if request.method == "POST":
        caption = request.POST.get("caption", "")
        media_file = request.FILES.get("media")
        
        if not media_file:
            return JsonResponse({"error": "Media file is required"}, status=400)
        
        # Validate file type
        allowed_types = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_VIDEO_TYPES
        is_valid, message = validate_media_file(media_file, allowed_types)
        if not is_valid:
            return JsonResponse({"error": message}, status=400)
        
        # Determine media type
        media_type = 'image' if media_file.content_type in settings.ALLOWED_IMAGE_TYPES else 'video'
        
        # Create story
        story = Story.objects.create(
            creator=request.user,
            media_url=media_file,
            media_type=media_type,
            caption=caption
        )
        
        return JsonResponse({
            "success": True,
            "story_id": story.id,
            "message": "Story created successfully",
            "expires_at": story.expires_at.strftime("%b %d, %Y %I:%M %p")
        })
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def get_stories(request):
    """Get all active stories from friends and self"""
    # Get friends
    friends = get_friends(request.user)
    friends.append(request.user)  # Include own stories
    
    # Get active stories
    stories = Story.objects.filter(
        creator__in=friends,
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    
    data = []
    for story in stories:
        # Check if user has viewed this story
        has_viewed = StoryView.objects.filter(story=story, viewer=request.user).exists()
        
        data.append({
            "id": story.id,
            "creator": story.creator.username,
            "media_type": story.media_type,
            "media_url": story.media_url.url,
            "caption": story.caption,
            "created_at": story.created_at.strftime("%b %d, %Y %I:%M %p"),
            "expires_at": story.expires_at.strftime("%b %d, %Y %I:%M %p"),
            "view_count": story.view_count,
            "has_viewed": has_viewed,
            "is_own_story": story.creator == request.user
        })
    
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def view_story(request, story_id):
    """View a story and track the view"""
    story = get_object_or_404(Story, id=story_id)
    
    # Check if story is expired
    if story.is_expired:
        return JsonResponse({"error": "Story has expired"}, status=410)
    
    # Track view (don't track own views)
    if story.creator != request.user:
        StoryView.objects.get_or_create(story=story, viewer=request.user)
    
    return JsonResponse({
        "success": True,
        "media_url": story.media_url.url,
        "media_type": story.media_type,
        "caption": story.caption,
        "creator": story.creator.username,
        "created_at": story.created_at.strftime("%b %d, %Y %I:%M %p")
    })


@login_required
def get_story_views(request, story_id):
    """Get list of users who viewed a story"""
    story = get_object_or_404(Story, id=story_id, creator=request.user)
    
    views = StoryView.objects.filter(story=story).order_by('-viewed_at')
    
    data = []
    for view in views:
        data.append({
            "viewer": view.viewer.username,
            "viewed_at": view.viewed_at.strftime("%b %d, %Y %I:%M %p")
        })
    
    return JsonResponse({
        "story_id": story.id,
        "total_views": len(data),
        "views": data
    })


@csrf_exempt
@login_required
def delete_story(request, story_id):
    """Delete own story"""
    if request.method == "DELETE" or request.method == "POST":
        story = get_object_or_404(Story, id=story_id, creator=request.user)
        
        # Delete media file
        if story.media_url:
            story.media_url.delete()
        
        story.delete()
        
        return JsonResponse({"success": True, "message": "Story deleted"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


# ========================================
# MESSAGE VIEWS
# ========================================

@csrf_exempt
@login_required
def send_message(request):
    """Send a message to a friend"""
    if request.method == "POST":
        receiver_username = request.POST.get("receiver")
        content = request.POST.get("content", "")
        media_file = request.FILES.get("media")
        
        if not receiver_username:
            return JsonResponse({"error": "Receiver is required"}, status=400)
        
        if not content and not media_file:
            return JsonResponse({"error": "Message content or media is required"}, status=400)
        
        # Get receiver
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
        # Validate media if provided
        if media_file:
            allowed_types = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_VIDEO_TYPES
            is_valid, message = validate_media_file(media_file, allowed_types)
            if not is_valid:
                return JsonResponse({"error": message}, status=400)
        
        # Create message
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            media=media_file
        )
        
        return JsonResponse({
            "success": True,
            "message_id": message.id,
            "sent_at": message.sent_at.strftime("%b %d, %Y %I:%M %p")
        })
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def get_messages(request, username):
    """Get message thread with a specific user"""
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('sent_at')
    
    # Mark received messages as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    data = []
    for msg in messages:
        data.append({
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "media_url": msg.media.url if msg.media else None,
            "sent_at": msg.sent_at.strftime("%b %d, %Y %I:%M %p"),
            "is_read": msg.is_read,
            "is_own_message": msg.sender == request.user
        })
    
    return JsonResponse(data, safe=False)


@login_required
def get_conversations(request):
    """Get list of all conversations"""
    # Get all users the current user has exchanged messages with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    
    user_ids = set(list(sent_to) + list(received_from))
    users = User.objects.filter(id__in=user_ids)
    
    data = []
    for user in users:
        # Get last message
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by('-sent_at').first()
        
        # Count unread messages
        unread_count = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()
        
        data.append({
            "username": user.username,
            "last_message": last_message.content[:50] if last_message else "",
            "last_message_time": last_message.sent_at.strftime("%b %d, %Y %I:%M %p") if last_message else "",
            "unread_count": unread_count
        })
    
    # Sort by last message time
    data.sort(key=lambda x: x["last_message_time"], reverse=True)
    
    return JsonResponse(data, safe=False)


@login_required
def mark_message_read(request, message_id):
    """Mark a message as read"""
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    
    if not message.is_read:
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
    
    return JsonResponse({"success": True})


# ========================================
# FRIENDSHIP VIEWS
# ========================================

@login_required
def get_friends_list(request):
    """Get list of all friends"""
    friends = get_friends(request.user)
    
    data = []
    for friend in friends:
        # Get last message
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=friend) |
            Q(sender=friend, receiver=request.user)
        ).order_by('-sent_at').first()
        
        data.append({
            "username": friend.username,
            "email": friend.email,
            "last_interaction": last_message.sent_at.strftime("%b %d, %Y %I:%M %p") if last_message else None
        })
    
    return JsonResponse(data, safe=False)
