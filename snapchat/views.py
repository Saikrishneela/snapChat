from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
from django.utils import timezone
from django.utils.dateformat import format as date_format
from datetime import datetime
from .models import Chat, FriendRequest
import pytz, random


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
