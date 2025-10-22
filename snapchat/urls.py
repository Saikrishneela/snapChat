from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('send-email/', views.send_welcome_email, name='send_email'),
    path("get-chats/", views.get_chats, name="get_chat"),
    path("add-chat/", views.add_chat, name="add_chat"),
    path("send-request/", views.send_request, name="send_request"),
    path("pending-requests/", views.get_pending_requests, name="pending_requests"),
    path("accept-request/", views.accept_request, name="accept_request"),
    path('', views.home, name='home'),  
]
