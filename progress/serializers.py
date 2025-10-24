from rest_framework import serializers
from .models import (
    Attendance, Assignment, AssignmentSubmission, Grade, StudyPlan,
    StudyPlanItem, StudentProgress, Achievement
)
from courses.serializers import SubjectSerializer
from authentication.serializers import UserSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model
    """
    student = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    marked_by = UserSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    marked_by_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'student_id', 'date', 'status', 'subject',
            'subject_id', 'remarks', 'marked_by', 'marked_by_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Assignment model
    """
    subject = SubjectSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(many=True, read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    assigned_by_id = serializers.IntegerField(write_only=True)
    assigned_to_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    submissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'subject', 'subject_id',
            'assigned_by', 'assigned_by_id', 'assigned_to', 'assigned_to_ids',
            'due_date', 'max_marks', 'attachment', 'is_published',
            'submissions_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_submissions_count(self, obj):
        return obj.submissions.count()


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for AssignmentSubmission model
    """
    assignment = AssignmentSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    graded_by = UserSerializer(read_only=True)
    assignment_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)
    graded_by_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_id', 'student', 'student_id',
            'submission_text', 'submission_file', 'submitted_at',
            'marks_obtained', 'feedback', 'graded_by', 'graded_by_id', 'graded_at'
        ]
        read_only_fields = ['id', 'submitted_at', 'graded_at']


class GradeSerializer(serializers.ModelSerializer):
    """
    Serializer for Grade model
    """
    student = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    graded_by = UserSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    graded_by_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'student_id', 'subject', 'subject_id',
            'grade_type', 'title', 'max_marks', 'marks_obtained',
            'percentage', 'grade_letter', 'remarks', 'graded_by',
            'graded_by_id', 'graded_at'
        ]
        read_only_fields = ['id', 'graded_at']


class StudyPlanItemSerializer(serializers.ModelSerializer):
    """
    Serializer for StudyPlanItem model
    """
    class Meta:
        model = StudyPlanItem
        fields = [
            'id', 'title', 'description', 'scheduled_date', 'scheduled_time',
            'duration_minutes', 'is_completed', 'completed_at', 'order'
        ]
        read_only_fields = ['id', 'completed_at']


class StudyPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for StudyPlan model
    """
    student = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    items = StudyPlanItemSerializer(many=True, read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    completed_items_count = serializers.SerializerMethodField()
    total_items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyPlan
        fields = [
            'id', 'student', 'student_id', 'title', 'description',
            'subject', 'subject_id', 'start_date', 'end_date',
            'is_active', 'items', 'completed_items_count', 'total_items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_completed_items_count(self, obj):
        return obj.items.filter(is_completed=True).count()
    
    def get_total_items_count(self, obj):
        return obj.items.count()


class StudentProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentProgress model
    """
    student = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StudentProgress
        fields = [
            'id', 'student', 'student_id', 'subject', 'subject_id',
            'overall_percentage', 'assignments_completed', 'total_assignments',
            'quizzes_taken', 'average_quiz_score', 'attendance_percentage',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for Achievement model
    """
    student = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'student', 'student_id', 'title', 'description',
            'achievement_type', 'subject', 'subject_id', 'icon',
            'points', 'earned_at'
        ]
        read_only_fields = ['id', 'earned_at']


class AttendanceSummarySerializer(serializers.Serializer):
    """
    Serializer for attendance summary
    """
    subject_name = serializers.CharField()
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()


class StudentDashboardSerializer(serializers.Serializer):
    """
    Serializer for student dashboard data
    """
    user = UserSerializer()
    overall_progress = serializers.FloatField()
    active_courses = serializers.IntegerField()
    completed_assignments = serializers.IntegerField()
    pending_assignments = serializers.IntegerField()
    quizzes_taken = serializers.IntegerField()
    average_quiz_score = serializers.FloatField()
    attendance_percentage = serializers.FloatField()
    recent_achievements = AchievementSerializer(many=True)
    upcoming_assignments = AssignmentSerializer(many=True)
    study_plans = StudyPlanSerializer(many=True)


class ParentDashboardSerializer(serializers.Serializer):
    """
    Serializer for parent dashboard data
    """
    user = UserSerializer()
    children = UserSerializer(many=True)
    children_progress = serializers.ListField(
        child=serializers.DictField()
    )
    recent_notifications = serializers.ListField(
        child=serializers.DictField()
    )
    upcoming_events = serializers.ListField(
        child=serializers.DictField()
    )
