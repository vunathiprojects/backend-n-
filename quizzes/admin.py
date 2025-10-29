from django.contrib import admin
from .models import (
    Quiz, Question, QuestionOption, QuizAttempt, QuizAnswer,
    QuizResult, QuizAnalytics
)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    search_fields = ('question_text',)
    inlines = [QuestionOptionInline]


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('option_text',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('get_quiz_title', 'score')
    search_fields = ('quiz__title',)

    def get_quiz_title(self, obj):
        return obj.quiz.title if hasattr(obj, 'quiz') and obj.quiz else "-"
    get_quiz_title.short_description = 'Quiz'


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('get_question_text', 'get_selected_option', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('question__question_text',)

    def get_question_text(self, obj):
        return obj.question.question_text if hasattr(obj, 'question') and obj.question else "-"
    get_question_text.short_description = 'Question'

    def get_selected_option(self, obj):
        return obj.selected_option.option_text if hasattr(obj, 'selected_option') and obj.selected_option else "-"
    get_selected_option.short_description = 'Selected Option'


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('get_quiz_title', 'total_questions', 'correct_answers', 'accuracy_percentage')
    search_fields = ('attempt__quiz__title',)

    def get_quiz_title(self, obj):
        if hasattr(obj, 'attempt') and hasattr(obj.attempt, 'quiz') and obj.attempt.quiz:
            return obj.attempt.quiz.title
        return "-"
    get_quiz_title.short_description = 'Quiz'


@admin.register(QuizAnalytics)
class QuizAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'total_attempts', 'average_score', 'pass_rate')
    search_fields = ('quiz__title',)
