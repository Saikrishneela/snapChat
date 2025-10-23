from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('sender', 'receiver')
        indexes = [
            models.Index(fields=['receiver', 'is_accepted']),
            models.Index(fields=['sender']),
        ]

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({'Accepted' if self.is_accepted else 'Pending'})"


class Friendship(models.Model):
    """Represents a mutual friendship between two users"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships_initiated")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships_received")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user1', 'user2')
        indexes = [
            models.Index(fields=['user1']),
            models.Index(fields=['user2']),
        ]

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}"


class Message(models.Model):
    """Direct messages between users"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    media = models.FileField(upload_to='messages/', null=True, blank=True)
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['-sent_at']),
        ]

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:30]}"


class Snap(models.Model):
    """Temporary photo/video snaps that disappear after viewing"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_snaps")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_snaps")
    media_url = models.FileField(upload_to='snaps/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    caption = models.CharField(max_length=200, blank=True)
    sent_at = models.DateTimeField(default=timezone.now)
    duration_seconds = models.IntegerField(default=10)  # How long snap is visible
    is_opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['receiver', 'is_opened']),
            models.Index(fields=['-sent_at']),
        ]

    def __str__(self):
        return f"Snap from {self.sender.username} to {self.receiver.username}"

    @property
    def is_expired(self):
        """Check if snap has been opened and expired"""
        if self.is_opened and self.opened_at:
            expiry_time = self.opened_at + timedelta(seconds=self.duration_seconds)
            return timezone.now() > expiry_time
        return False


class SnapView(models.Model):
    """Track when snaps are viewed"""
    snap = models.ForeignKey(Snap, on_delete=models.CASCADE, related_name="views")
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="snap_views")
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('snap', 'viewer')
        indexes = [
            models.Index(fields=['snap']),
            models.Index(fields=['viewer']),
        ]

    def __str__(self):
        return f"{self.viewer.username} viewed snap at {self.viewed_at}"


class Story(models.Model):
    """24-hour stories visible to all friends"""
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    media_url = models.FileField(upload_to='stories/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Stories"
        indexes = [
            models.Index(fields=['creator', '-created_at']),
            models.Index(fields=['expires_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Story by {self.creator.username} at {self.created_at}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def view_count(self):
        return self.story_views.count()


class StoryView(models.Model):
    """Track who viewed stories"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="story_views")
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewed_stories")
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('story', 'viewer')
        indexes = [
            models.Index(fields=['story']),
            models.Index(fields=['viewer']),
        ]

    def __str__(self):
        return f"{self.viewer.username} viewed story at {self.viewed_at}"
