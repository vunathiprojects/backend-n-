from django.db import models
from authentication.models import User


class AIStudyPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='student_id'
    )
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=200)
    subtopic = models.CharField(max_length=200, null=True, blank=True)
    plan_title = models.CharField(max_length=200)
    plan_content = models.TextField()
    plan_type = models.CharField(max_length=50, default='study_plan')
    difficulty_level = models.CharField(max_length=20, default='medium')
    estimated_duration_hours = models.IntegerField(default=1)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_study_plans'
        verbose_name = 'AI Study Plan'
        verbose_name_plural = 'AI Study Plans'

    def __str__(self):
        return f"{self.plan_title} - {self.student_id}"


class AIGeneratedNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='student_id'
    )
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=200)
    subtopic = models.CharField(max_length=200, null=True, blank=True)
    note_title = models.CharField(max_length=200)
    note_content = models.TextField()
    note_type = models.CharField(max_length=50, default='ai_generated')
    key_points = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_generated_notes'
        verbose_name = 'AI Generated Note'
        verbose_name_plural = 'AI Generated Notes'

    def __str__(self):
        return f"{self.note_title} - {self.student_id}"


class ManualNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='student_id'
    )
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=200)
    subtopic = models.CharField(max_length=200, null=True, blank=True)
    note_title = models.CharField(max_length=200, null=True, blank=True)
    note_content = models.TextField()
    note_type = models.CharField(max_length=50, default='manual')
    color = models.CharField(max_length=7, default='#fef3c7')
    is_important = models.BooleanField(default=False)
    tags = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manual_notes'
        verbose_name = 'Manual Note'
        verbose_name_plural = 'Manual Notes'

    def __str__(self):
        return f"Manual Note - {self.student_id} - {self.created_at}"


class AIChatHistory(models.Model):
    chat_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='student_id'
    )
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=200)
    subtopic = models.CharField(max_length=200, null=True, blank=True)
    user_message = models.TextField()
    ai_response = models.TextField()
    response_type = models.CharField(max_length=50, default='general')
    message_timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = 'ai_chat_history'
        verbose_name = 'AI Chat History'
        verbose_name_plural = 'AI Chat History'

    def __str__(self):
        return f"Chat - {self.student_id} - {self.message_timestamp}"


class AIInteractionSession(models.Model):
    session_id = models.CharField(max_length=100, primary_key=True)
    student_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='student_id'
    )
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=200)
    subtopic = models.CharField(max_length=200, null=True, blank=True)
    session_type = models.CharField(max_length=50, default='general')
    total_messages = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ai_interaction_sessions'
        verbose_name = 'AI Interaction Session'
        verbose_name_plural = 'AI Interaction Sessions'

    def __str__(self):
        return f"Session {self.session_id} - {self.student_id}"


class AIFavorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='student_id'
    )
    content_type = models.CharField(max_length=50)  # 'study_plan', 'note', 'chat'
    content_id = models.IntegerField()
    favorite_title = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_favorites'
        verbose_name = 'AI Favorite'
        verbose_name_plural = 'AI Favorites'

    def __str__(self):
        return f"Favorite - {self.content_type} - {self.student_id}"
