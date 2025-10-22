# Generated manually for new features
# To apply this migration, run: python manage.py migrate

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snapchat', '0006_friendrequest'),
    ]

    operations = [
        # Update FriendRequest model with Meta options
        migrations.AlterModelOptions(
            name='friendrequest',
            options={},
        ),
        migrations.AddIndex(
            model_name='friendrequest',
            index=models.Index(fields=['receiver', 'is_accepted'], name='snapchat_fr_receiver_idx'),
        ),
        migrations.AddIndex(
            model_name='friendrequest',
            index=models.Index(fields=['sender'], name='snapchat_fr_sender_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together={('sender', 'receiver')},
        ),
        
        # Create Friendship model
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships_initiated', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.AddIndex(
            model_name='friendship',
            index=models.Index(fields=['user1'], name='snapchat_friendship_user1_idx'),
        ),
        migrations.AddIndex(
            model_name='friendship',
            index=models.Index(fields=['user2'], name='snapchat_friendship_user2_idx'),
        ),
        
        # Create Message model
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('media', models.FileField(blank=True, null=True, upload_to='messages/')),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['sender', 'receiver'], name='snapchat_message_sender_receiver_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['-sent_at'], name='snapchat_message_sent_at_idx'),
        ),
        
        # Create Snap model
        migrations.CreateModel(
            name='Snap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_url', models.FileField(upload_to='snaps/%Y/%m/%d/')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration_seconds', models.IntegerField(default=10)),
                ('is_opened', models.BooleanField(default=False)),
                ('opened_at', models.DateTimeField(blank=True, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_snaps', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_snaps', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
        migrations.AddIndex(
            model_name='snap',
            index=models.Index(fields=['receiver', 'is_opened'], name='snapchat_snap_receiver_opened_idx'),
        ),
        migrations.AddIndex(
            model_name='snap',
            index=models.Index(fields=['-sent_at'], name='snapchat_snap_sent_at_idx'),
        ),
        
        # Create SnapView model
        migrations.CreateModel(
            name='SnapView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('snap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='snapchat.snap')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snap_views', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('snap', 'viewer')},
            },
        ),
        migrations.AddIndex(
            model_name='snapview',
            index=models.Index(fields=['snap'], name='snapchat_snapview_snap_idx'),
        ),
        migrations.AddIndex(
            model_name='snapview',
            index=models.Index(fields=['viewer'], name='snapchat_snapview_viewer_idx'),
        ),
        
        # Create Story model
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_url', models.FileField(upload_to='stories/%Y/%m/%d/')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expires_at', models.DateTimeField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stories',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='story',
            index=models.Index(fields=['creator', '-created_at'], name='snapchat_story_creator_created_idx'),
        ),
        migrations.AddIndex(
            model_name='story',
            index=models.Index(fields=['expires_at'], name='snapchat_story_expires_idx'),
        ),
        
        # Create StoryView model
        migrations.CreateModel(
            name='StoryView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_views', to='snapchat.story')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_stories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('story', 'viewer')},
            },
        ),
        migrations.AddIndex(
            model_name='storyview',
            index=models.Index(fields=['story'], name='snapchat_storyview_story_idx'),
        ),
        migrations.AddIndex(
            model_name='storyview',
            index=models.Index(fields=['viewer'], name='snapchat_storyview_viewer_idx'),
        ),
    ]

