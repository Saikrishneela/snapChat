from django.contrib import admin
from .models import Chat, FriendRequest, Friendship, Message, Snap, SnapView, Story, StoryView


# ----------------------------
# Chat Admin
# ----------------------------
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'name', 'user', 'time')
    search_fields = ('name', 'user__username')
    list_filter = ('time',)
    ordering = ('-time',)
    
    def get_model_perms(self, request):
        """
        Control access for different users:
        - Mahesh Babu (superuser) → full access
        - Saikrishna → view-only access
        """
        perms = super().get_model_perms(request)
        username = request.user.username.lower()
        
        if username == "saikrishna":
            perms['add'] = False
            perms['change'] = False
            perms['delete'] = False
        
        return perms


# ----------------------------
# Friend Request Admin
# ----------------------------
@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_accepted', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('is_accepted', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


# ----------------------------
# Friendship Admin
# ----------------------------
@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


# ----------------------------
# Message Admin
# ----------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content_preview', 'sent_at', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read', 'sent_at')
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at', 'read_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


# ----------------------------
# Snap Admin
# ----------------------------
@admin.register(Snap)
class SnapAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'media_type', 'sent_at', 'is_opened', 'is_expired')
    search_fields = ('sender__username', 'receiver__username', 'caption')
    list_filter = ('media_type', 'is_opened', 'sent_at')
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at', 'opened_at', 'is_expired')
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


# ----------------------------
# Snap View Admin
# ----------------------------
@admin.register(SnapView)
class SnapViewAdmin(admin.ModelAdmin):
    list_display = ('snap', 'viewer', 'viewed_at')
    search_fields = ('snap__sender__username', 'snap__receiver__username', 'viewer__username')
    list_filter = ('viewed_at',)
    ordering = ('-viewed_at',)
    readonly_fields = ('viewed_at',)


# ----------------------------
# Story Admin
# ----------------------------
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('creator', 'media_type', 'created_at', 'expires_at', 'view_count', 'is_expired')
    search_fields = ('creator__username', 'caption')
    list_filter = ('media_type', 'created_at', 'expires_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'view_count', 'is_expired')
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


# ----------------------------
# Story View Admin
# ----------------------------
@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ('story', 'viewer', 'viewed_at')
    search_fields = ('story__creator__username', 'viewer__username')
    list_filter = ('viewed_at',)
    ordering = ('-viewed_at',)
    readonly_fields = ('viewed_at',)