from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    
    # Pages
    path('messages.html', views.messages_page, name='messages_page'),
    path('snaps.html', views.snaps_page, name='snaps_page'),
    
    # Email
    path('send-email/', views.send_welcome_email, name='send_email'),
    
    # Chat (legacy)
    path("get-chats/", views.get_chats, name="get_chat"),
    path("add-chat/", views.add_chat, name="add_chat"),
    
    # Friend Requests
    path("send-request/", views.send_request, name="send_request"),
    path("pending-requests/", views.get_pending_requests, name="pending_requests"),
    path("accept-request/", views.accept_request, name="accept_request"),
    
    # Friends
    path("friends/", views.get_friends_list, name="friends_list"),
    
    # Snaps
    path("snap/send/", views.send_snap, name="send_snap"),
    path("snap/received/", views.get_received_snaps, name="received_snaps"),
    path("snap/sent/", views.get_sent_snaps, name="sent_snaps"),
    path("snap/view/<int:snap_id>/", views.view_snap, name="view_snap"),
    
    # Stories
    path("story/create/", views.create_story, name="create_story"),
    path("story/all/", views.get_stories, name="get_stories"),
    path("story/view/<int:story_id>/", views.view_story, name="view_story"),
    path("story/views/<int:story_id>/", views.get_story_views, name="story_views"),
    path("story/delete/<int:story_id>/", views.delete_story, name="delete_story"),
    
    # Messages
    path("message/send/", views.send_message, name="send_message"),
    path("message/conversations/", views.get_conversations, name="conversations"),
    path("message/thread/<str:username>/", views.get_messages, name="get_messages"),
    path("message/read/<int:message_id>/", views.mark_message_read, name="mark_message_read"),
]
