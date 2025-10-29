from django.contrib import admin
from .models import Event, EventRegistration, Notification, Announcement, Message, Feedback


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'end_date', 'location', 'is_published')
    list_filter = ('event_type', 'is_published', 'start_date')
    search_fields = ('title', 'description', 'location')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registered_at', 'status')
    list_filter = ('status', 'registered_at')
    search_fields = ('event__title', 'user__username')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notification_type', 'is_read', 'created_at')  # removed 'priority'
    list_filter = ('notification_type', 'is_read', 'created_at')  # removed 'priority'
    search_fields = ('title', 'message', 'recipient__username')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_audience', 'is_published', 'created_at')  # removed 'author', 'is_important'
    list_filter = ('target_audience', 'is_published', 'created_at')  # removed 'is_important'
    search_fields = ('title', 'content')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'is_read', 'created_at')  # removed 'is_important'
    list_filter = ('is_read', 'created_at')  # removed 'is_important'
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'subject', 'is_resolved', 'created_at')  # removed 'is_anonymous'
    list_filter = ('feedback_type', 'is_resolved', 'created_at')  # removed 'is_anonymous'
    search_fields = ('subject', 'message', 'user__username')
