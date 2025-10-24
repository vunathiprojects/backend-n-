from rest_framework import serializers
from .models import (
    Subject, Course, Chapter, Lesson, CourseEnrollment, 
    LessonProgress, CourseMaterial
)
from authentication.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Subject model
    """
    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'description', 'icon', 'color',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseMaterial model
    """
    class Meta:
        model = CourseMaterial
        fields = [
            'id', 'title', 'description', 'material_type', 'file',
            'is_required', 'order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson model
    """
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'lesson_type', 'content',
            'video_url', 'video_file', 'duration_minutes', 'order',
            'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChapterSerializer(serializers.ModelSerializer):
    """
    Serializer for Chapter model
    """
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chapter
        fields = [
            'id', 'title', 'description', 'chapter_number', 'order',
            'is_published', 'lessons', 'lessons_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_lessons_count(self, obj):
        return obj.lessons.filter(is_published=True).count()


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """
    instructor = UserSerializer(read_only=True)
    instructor_id = serializers.IntegerField(write_only=True, required=False)
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    chapters_count = serializers.SerializerMethodField()
    materials = CourseMaterialSerializer(many=True, read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'subject', 'subject_id', 'grade',
            'instructor', 'instructor_id', 'thumbnail', 'duration_hours',
            'is_published', 'chapters', 'chapters_count', 'materials',
            'enrollment_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_chapters_count(self, obj):
        return obj.chapters.filter(is_published=True).count()
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(is_active=True).count()


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseEnrollment model
    """
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CourseEnrollment
        fields = [
            'id', 'student', 'student_id', 'course', 'course_id',
            'enrolled_at', 'is_active', 'progress_percentage', 'last_accessed'
        ]
        read_only_fields = ['id', 'enrolled_at', 'last_accessed']


class LessonProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for LessonProgress model
    """
    student = UserSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    lesson_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'student', 'student_id', 'lesson', 'lesson_id',
            'is_completed', 'completion_percentage', 'time_spent_minutes',
            'last_accessed', 'completed_at'
        ]
        read_only_fields = ['id', 'last_accessed', 'completed_at']


class CourseListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for course listing
    """
    subject = SubjectSerializer(read_only=True)
    instructor = UserSerializer(read_only=True)
    chapters_count = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'subject', 'grade',
            'instructor', 'thumbnail', 'duration_hours',
            'chapters_count', 'enrollment_count', 'created_at'
        ]
    
    def get_chapters_count(self, obj):
        return obj.chapters.filter(is_published=True).count()
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(is_active=True).count()


class CourseDetailSerializer(CourseSerializer):
    """
    Detailed serializer for course with all related data
    """
    pass


class StudentCourseProgressSerializer(serializers.Serializer):
    """
    Serializer for student course progress summary
    """
    course_id = serializers.IntegerField()
    course_title = serializers.CharField()
    subject_name = serializers.CharField()
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    progress_percentage = serializers.FloatField()
    last_accessed = serializers.DateTimeField()
    enrollment_date = serializers.DateTimeField()
