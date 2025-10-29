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
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Question model
    """
    list_display = ('question_text', 'quiz')
    search_fields = ('question_text',)
    inlines = [QuestionOptionInline]


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuestionOption model
    """
    list_display = ('option_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('option_text',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAttempt model
    """
    list_display = ('quiz', 'score')
    search_fields = ('quiz__title',)


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAnswer model
    """
    list_display = ('question', 'selected_option', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('question__question_text',)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizResult model
    """
    list_display = ('quiz', 'total_questions', 'correct_answers', 'accuracy_percentage')
    search_fields = ('quiz__title',)


@admin.register(QuizAnalytics)
class QuizAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizAnalytics model
    """
    list_display = ('quiz', 'total_attempts', 'average_score', 'pass_rate')
    search_fields = ('quiz__title',)
