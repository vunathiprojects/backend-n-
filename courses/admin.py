from django.contrib import admin
from .models import (
    Subject, Course, Chapter, Lesson, CourseEnrollment,
    LessonProgress, CourseMaterial
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Subject model
    """
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for Course model
    """
    list_display = ('title', 'subject', 'grade', 'instructor', 'duration_hours', 'is_published', 'created_at')
    list_filter = ('subject', 'grade', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('instructor',)
    filter_horizontal = ()


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    """
    Admin configuration for Chapter model
    """
    list_display = ('title', 'course', 'chapter_number', 'order', 'is_published')
    list_filter = ('course', 'is_published')
    search_fields = ('title', 'description')
    raw_id_fields = ('course',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for Lesson model
    """
    list_display = ('title', 'chapter', 'lesson_type', 'duration_minutes', 'order', 'is_published')
    list_filter = ('lesson_type', 'is_published', 'chapter__course')
    search_fields = ('title', 'description')
    raw_id_fields = ('chapter',)


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for CourseEnrollment model
    """
    list_display = ('student', 'course', 'enrolled_at', 'is_active', 'progress_percentage')
    list_filter = ('is_active', 'enrolled_at', 'course__subject')
    search_fields = ('student__username', 'course__title')
    raw_id_fields = ('student', 'course')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for LessonProgress model
    """
    list_display = ('student', 'lesson', 'is_completed', 'completion_percentage', 'time_spent_minutes', 'last_accessed')
    list_filter = ('is_completed', 'lesson__chapter__course')
    search_fields = ('student__username', 'lesson__title')
    raw_id_fields = ('student', 'lesson')


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    """
    Admin configuration for CourseMaterial model
    """
    list_display = ('title', 'course', 'material_type', 'is_required', 'order')
    list_filter = ('material_type', 'is_required', 'course')
    search_fields = ('title', 'description')
    raw_id_fields = ('course',)
