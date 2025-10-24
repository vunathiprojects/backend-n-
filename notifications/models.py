from django.db import models
from authentication.models import User, Student
from courses.models import Course, Topic


class Review(models.Model):
    """
    Review model matching existing schema
    """
    review_id = models.AutoField(primary_key=True)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    instructor_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='instructor_reviews')
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.reviewer_id.firstname} - {self.created_at}"
    
    class Meta:
        db_table = 'review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Rating(models.Model):
    """
    Rating model matching existing schema
    """
    rating_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    instructor_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='instructor_ratings')
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    rating_value = models.IntegerField()  # 1-5 rating
    rated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_id.firstname} - {self.rating_value} stars"
    
    class Meta:
        db_table = 'rating'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Report(models.Model):
    """
    Report model matching existing schema
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    REPORT_TYPES = [
        ('content', 'Content Issue'),
        ('user', 'User Behavior'),
        ('technical', 'Technical Issue'),
        ('other', 'Other'),
    ]
    
    report_id = models.AutoField(primary_key=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    reference_id = models.IntegerField()  # ID of the reported item
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Report by {self.reported_by.firstname} - {self.report_type}"
    
    class Meta:
        db_table = 'report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


# Legacy models for backward compatibility (if needed)
class Event(models.Model):
    """
    Event model for backward compatibility
    """
    EVENT_TYPES = [
        ('class', 'Class'),
        ('exam', 'Exam'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]
    
    TARGET_AUDIENCES = [
        ('all', 'All Users'),
        ('students', 'Students'),
        ('parents', 'Parents'),
        ('teachers', 'Teachers'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCES, default='all')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    registration_required = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class EventRegistration(models.Model):
    """
    Event Registration model for backward compatibility
    """
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.firstname} - {self.event.title}"
    
    class Meta:
        db_table = 'event_registrations'
        unique_together = ['event', 'user']
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'


class Notification(models.Model):
    """
    Notification model for backward compatibility
    """
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recipient.firstname} - {self.title}"
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class Announcement(models.Model):
    """
    Announcement model for backward compatibility
    """
    TARGET_AUDIENCES = [
        ('all', 'All Users'),
        ('students', 'Students'),
        ('parents', 'Parents'),
        ('teachers', 'Teachers'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCES, default='all')
    is_important = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'


class Message(models.Model):
    """
    Message model for backward compatibility
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.firstname} to {self.recipient.firstname} - {self.subject}"
    
    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Feedback(models.Model):
    """
    Feedback model for backward compatibility
    """
    FEEDBACK_TYPES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('improvement', 'Improvement Suggestion'),
        ('general', 'General Feedback'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, default='medium')
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.firstname} - {self.subject}"
    
    class Meta:
        db_table = 'feedback'
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'