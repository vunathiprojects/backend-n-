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
    list_display = ('title', 'description', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    # Removed: subject, grade, difficulty, duration_minutes, total_questions, is_premium, created_by (do not exist)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Question model
    """
    list_display = ('question_text', 'quiz', 'question_type', 'points', 'is_active')
    list_filter = ('question_type', 'is_active')
    search_fields = ('question_text',)
    inlines = [QuestionOptionInline]
    # Removed: quiz__subject (invalid)
    # Removed: raw_id_fields = ('quiz',) if quiz is not FK, you can add later if needed


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuestionOption model
    """
    list_display = ('option_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('option_text',)
    # Removed: question__quiz (invalid)
    # Removed: order (if not present)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAttempt model
    """
    list_display = ('quiz', 'score', 'is_passed', 'is_completed')
    list_filter = ('is_completed', 'is_passed')
    search_fields = ('quiz__title',)
    # Removed: student, started_at, completed_at, quiz__subject (invalid)
    # Removed: raw_id_fields & readonly_fields (invalid)


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAnswer model
    """
    list_display = ('quiz', 'question', 'selected_option', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('question__question_text',)
    # Removed: attempt, points_earned, answered_at (invalid)
    # Removed: raw_id_fields & readonly_fields (invalid)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizResult model
    """
    list_display = ('quiz', 'total_questions', 'correct_answers', 'accuracy_percentage', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('quiz__title',)
    # Removed: attempt, attempt__quiz__subject (invalid)
    # Removed: raw_id_fields & readonly_fields (invalid)


@admin.register(QuizAnalytics)
class QuizAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAnalytics model
    """
    list_display = ('quiz', 'total_attempts', 'average_score', 'pass_rate', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('quiz__title',)
    # Removed: quiz__subject (invalid)
