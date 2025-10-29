from django.contrib import admin
from .models import (
    Quiz, Question, QuestionOption, QuizAttempt, QuizAnswer,
    QuizResult, QuizAnalytics
)


class QuestionOptionInline(admin.TabularInline):
    """
    Inline admin for QuestionOption
    """
    model = QuestionOption
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin configuration for Quiz model
    """
    list_display = ('title', 'subject', 'grade', 'difficulty', 'duration_minutes', 'total_questions', 'is_published', 'created_at')
    list_filter = ('subject', 'grade', 'difficulty', 'is_published', 'is_premium', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('created_by',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Question model
    """
    list_display = ('question_text', 'quiz', 'question_type', 'points', 'order', 'is_active')
    list_filter = ('question_type', 'is_active', 'quiz__subject')
    search_fields = ('question_text',)
    raw_id_fields = ('quiz',)
    inlines = [QuestionOptionInline]


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuestionOption model
    """
    list_display = ('option_text', 'question', 'is_correct', 'order')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('option_text',)
    raw_id_fields = ('question',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAttempt model
    """
    list_display = ('student', 'quiz', 'started_at', 'completed_at', 'score', 'is_passed', 'is_completed')
    list_filter = ('is_completed', 'is_passed', 'started_at', 'quiz__subject')
    search_fields = ('student__username', 'quiz__title')
    raw_id_fields = ('student', 'quiz')
    readonly_fields = ('started_at', 'completed_at')


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAnswer model
    """
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct', 'answered_at', 'attempt__quiz')
    search_fields = ('attempt__student__username', 'question__question_text')
    raw_id_fields = ('attempt', 'question', 'selected_option')
    readonly_fields = ('answered_at',)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizResult model
    """
    list_display = ('attempt', 'total_questions', 'correct_answers', 'accuracy_percentage', 'created_at')
    list_filter = ('created_at', 'attempt__quiz__subject')
    search_fields = ('attempt__student__username', 'attempt__quiz__title')
    raw_id_fields = ('attempt',)
    readonly_fields = ('created_at',)


@admin.register(QuizAnalytics)
class QuizAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAnalytics model
    """
    list_display = ('quiz', 'total_attempts', 'average_score', 'pass_rate', 'last_updated')
    list_filter = ('last_updated', 'quiz__subject')
    search_fields = ('quiz__title',)
    raw_id_fields = ('quiz',)
    readonly_fields = ('last_updated',)
