from django.contrib import admin
from .models import (
    Course,
    Topic,
    PDFFiles,
    VideoFiles,
    Subject,
    Chapter,
    Lesson,
    CourseEnrollment,
    LessonProgress,
    CourseMaterial
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name', 'class_id', 'course_price')
    search_fields = ('course_name',)
    list_filter = ('class_id',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_id', 'topic_name', 'course_id')
    search_fields = ('topic_name',)


@admin.register(PDFFiles)
class PDFFilesAdmin(admin.ModelAdmin):
    list_display = ('pdf_id', 'title', 'course_id', 'topic_id', 'file_name', 'file_type', 'is_public', 'uploaded_at')
    search_fields = ('title', 'file_name')
    list_filter = ('is_public', 'uploaded_at')


@admin.register(VideoFiles)
class VideoFilesAdmin(admin.ModelAdmin):
    list_display = ('video_id', 'title', 'course_id', 'topic_id', 'file_name', 'file_type', 'size_in_mb', 'is_public', 'uploaded_at')
    search_fields = ('title', 'file_name')
    list_filter = ('is_public', 'uploaded_at')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'chapter_number', 'order', 'is_published', 'created_at')
    search_fields = ('title', 'course__course_name')
    list_filter = ('is_published', 'created_at')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'lesson_type', 'order', 'is_published', 'duration_minutes')
    search_fields = ('title', 'chapter__title')
    list_filter = ('lesson_type', 'is_published')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'is_active', 'enrolled_at', 'last_accessed')
    search_fields = ('student__student__firstname', 'course__course_name')
    list_filter = ('is_active', 'enrolled_at')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completion_percentage', 'is_completed', 'last_accessed')
    search_fields = ('student__student__firstname', 'lesson__title')
    list_filter = ('is_completed', 'last_accessed')


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'is_public', 'created_at')
    search_fields = ('title', 'course__course_name')
    list_filter = ('material_type', 'is_public', 'created_at')
