from django.contrib import admin
from .models import (
    Event, EventRegistration, Notification, Announcement,
    Message, Feedback
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin configuration for Event model
    """
    list_display = ('title', 'event_type', 'start_date', 'end_date', 'location', 'organizer', 'target_audience', 'is_published', 'created_at')
    list_filter = ('event_type', 'target_audience', 'is_published', 'start_date', 'created_at')
    search_fields = ('title', 'description', 'location')
    raw_id_fields = ('organizer',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    """
    Admin configuration for EventRegistration model
    """
    list_display = ('event', 'user', 'registered_at', 'status')
    list_filter = ('status', 'registered_at', 'event__event_type')
    search_fields = ('event__title', 'user__username')
    raw_id_fields = ('event', 'user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model
    """
    list_display = ('title', 'recipient', 'notification_type', 'priority', 'is_read', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    raw_id_fields = ('recipient', 'sender')
    readonly_fields = ('created_at', 'read_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Admin configuration for Announcement model
    """
    list_display = ('title', 'author', 'target_audience', 'is_published', 'is_important', 'created_at')
    list_filter = ('target_audience', 'is_published', 'is_important', 'created_at')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for Message model
    """
    list_display = ('subject', 'sender', 'recipient', 'is_read', 'is_important', 'created_at')
    list_filter = ('is_read', 'is_important', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')
    raw_id_fields = ('sender', 'recipient', 'parent_message')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin configuration for Feedback model
    """
    list_display = ('user', 'feedback_type', 'subject', 'is_anonymous', 'is_resolved', 'created_at')
    list_filter = ('feedback_type', 'is_anonymous', 'is_resolved', 'created_at')
    search_fields = ('subject', 'message', 'user__username')
    raw_id_fields = ('user', 'responded_by')
    readonly_fields = ('created_at', 'responded_at')
