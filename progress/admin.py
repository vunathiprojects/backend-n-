from django.contrib import admin
from .models import (
    Assignment, AssignmentQuestion, AssignmentSubmission, AssignmentAnswer,
    CareerPerformance, MentorshipTicket, Attendance, Grade,
    StudentProgress, StudyPlan, StudyPlanItem, Achievement
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'topic_id', 'due_date', 'file_url')
    search_fields = ('description', 'topic_id__topic_name')
    list_filter = ('due_date',)
    ordering = ('-due_date',)


@admin.register(AssignmentQuestion)
class AssignmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'assignment_id', 'question_text', 'correct_option')
    search_fields = ('question_text', 'assignment_id__description')
    list_filter = ('correct_option',)
    ordering = ('assignment_id',)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'assignment_id', 'student_id', 'submitted_at', 'grade')
    search_fields = ('assignment_id__description', 'student_id__first_name')
    list_filter = ('submitted_at', 'grade')
    ordering = ('-submitted_at',)


@admin.register(AssignmentAnswer)
class AssignmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_id', 'submission_id', 'question_id', 'selected_option', 'is_correct')
    search_fields = ('submission_id__student_id__first_name', 'question_id__question_text')
    list_filter = ('is_correct',)
    ordering = ('submission_id',)


@admin.register(CareerPerformance)
class CareerPerformanceAdmin(admin.ModelAdmin):
    list_display = ('performance_id', 'student_id', 'avg_assignment_score', 'avg_mocktest_score', 'overall_rating', 'last_updated')
    search_fields = ('student_id__firstname',)
    list_filter = ('last_updated',)
    ordering = ('-last_updated',)


@admin.register(MentorshipTicket)
class MentorshipTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'title', 'student_id', 'instructor_id', 'status', 'created_at', 'resolved_at')
    search_fields = ('title', 'student_id__firstname', 'instructor_id__username')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'created_at')
    search_fields = ('student__firstname', 'course__course_name')
    list_filter = ('status', 'date')
    ordering = ('-date',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'assignment', 'grade_value', 'max_grade', 'grade_type', 'graded_by', 'graded_at')
    search_fields = ('student__firstname', 'course__course_name', 'graded_by__username')
    list_filter = ('grade_type', 'graded_at')
    ordering = ('-graded_at',)


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'overall_percentage', 'lessons_completed', 'assignments_completed', 'last_accessed')
    search_fields = ('student__firstname', 'course__course_name')
    list_filter = ('last_accessed',)
    ordering = ('-last_accessed',)


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'start_date', 'end_date', 'is_active', 'created_at')
    search_fields = ('student__firstname', 'title')
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-created_at',)


@admin.register(StudyPlanItem)
class StudyPlanItemAdmin(admin.ModelAdmin):
    list_display = ('study_plan', 'title', 'due_date', 'is_completed', 'order')
    search_fields = ('study_plan__title', 'title')
    list_filter = ('is_completed', 'due_date')
    ordering = ('order',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'achievement_type', 'points', 'earned_at')
    search_fields = ('student__firstname', 'title')
    list_filter = ('achievement_type', 'earned_at')
    ordering = ('-earned_at',)
