from django.contrib import admin
from .models import (
    Attendance, Assignment, AssignmentSubmission, Grade, StudyPlan,
    StudyPlanItem, StudentProgress, Achievement
)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Attendance model
    """
    list_display = ('student', 'date', 'subject', 'status', 'marked_by', 'created_at')
    list_filter = ('status', 'date', 'subject', 'created_at')
    search_fields = ('student__username', 'subject__name', 'remarks')
    raw_id_fields = ('student', 'subject', 'marked_by')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Assignment model
    """
    list_display = ('title', 'subject', 'assigned_by', 'due_date', 'max_marks', 'is_published', 'created_at')
    list_filter = ('subject', 'is_published', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('assigned_by', 'subject')
    filter_horizontal = ('assigned_to',)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    """
    Admin configuration for AssignmentSubmission model
    """
    list_display = ('assignment', 'student', 'submitted_at', 'marks_obtained', 'graded_by', 'graded_at')
    list_filter = ('submitted_at', 'graded_at', 'assignment__subject')
    search_fields = ('assignment__title', 'student__username')
    raw_id_fields = ('assignment', 'student', 'graded_by')
    readonly_fields = ('submitted_at', 'graded_at')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Grade model
    """
    list_display = ('student', 'subject', 'grade_type', 'title', 'marks_obtained', 'percentage', 'grade_letter', 'graded_at')
    list_filter = ('grade_type', 'subject', 'graded_at')
    search_fields = ('student__username', 'title', 'remarks')
    raw_id_fields = ('student', 'subject', 'graded_by')


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    """
    Admin configuration for StudyPlan model
    """
    list_display = ('title', 'student', 'subject', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('subject', 'is_active', 'start_date', 'end_date', 'created_at')
    search_fields = ('title', 'description', 'student__username')
    raw_id_fields = ('student', 'subject')


@admin.register(StudyPlanItem)
class StudyPlanItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for StudyPlanItem model
    """
    list_display = ('title', 'study_plan', 'scheduled_date', 'scheduled_time', 'duration_minutes', 'is_completed', 'order')
    list_filter = ('is_completed', 'scheduled_date', 'study_plan__subject')
    search_fields = ('title', 'description')
    raw_id_fields = ('study_plan',)


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for StudentProgress model
    """
    list_display = ('student', 'subject', 'overall_percentage', 'assignments_completed', 'total_assignments', 'quizzes_taken', 'attendance_percentage', 'last_updated')
    list_filter = ('subject', 'last_updated')
    search_fields = ('student__username', 'subject__name')
    raw_id_fields = ('student', 'subject')
    readonly_fields = ('last_updated',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """
    Admin configuration for Achievement model
    """
    list_display = ('student', 'title', 'achievement_type', 'subject', 'points', 'earned_at')
    list_filter = ('achievement_type', 'subject', 'earned_at')
    search_fields = ('student__username', 'title', 'description')
    raw_id_fields = ('student', 'subject')
    readonly_fields = ('earned_at',)
