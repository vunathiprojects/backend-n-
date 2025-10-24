from rest_framework import serializers
from .models import (
    AIStudyPlan, AIGeneratedNote, ManualNote, 
    AIChatHistory, AIInteractionSession, AIFavorite
)


class AIStudyPlanSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(max_length=50, default='Unknown Class')
    subject = serializers.CharField(max_length=100, default='Unknown Subject')
    chapter = serializers.CharField(max_length=200, default='Unknown Chapter')
    plan_title = serializers.CharField(max_length=200, default='Study Plan')
    plan_content = serializers.CharField(default='No content available')
    plan_type = serializers.CharField(max_length=50, default='study_plan')
    difficulty_level = serializers.CharField(max_length=20, default='medium')
    estimated_duration_hours = serializers.IntegerField(default=1)
    
    def validate_class_name(self, value):
        if not value or value == 'undefined' or value == 'Class undefined':
            return 'Unknown Class'
        return value.strip()
    
    def validate_subject(self, value):
        if not value or value == 'undefined':
            return 'Unknown Subject'
        return value.strip()
    
    def validate_chapter(self, value):
        if not value or value == 'undefined':
            return 'Unknown Chapter'
        return value.strip()
    
    def validate_plan_title(self, value):
        if not value or value == 'undefined':
            return 'Study Plan'
        return value.strip()
    
    def validate_plan_content(self, value):
        if not value or value == 'undefined':
            return 'No content available'
        return value.strip()
    
    class Meta:
        model = AIStudyPlan
        fields = [
            'plan_id', 'student_id', 'class_name', 'subject', 'chapter', 'subtopic',
            'plan_title', 'plan_content', 'plan_type', 'difficulty_level',
            'estimated_duration_hours', 'is_favorite', 'created_at', 'updated_at'
        ]
        read_only_fields = ['plan_id', 'created_at', 'updated_at']


class AIGeneratedNoteSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(max_length=50, default='Unknown Class')
    subject = serializers.CharField(max_length=100, default='Unknown Subject')
    chapter = serializers.CharField(max_length=200, default='Unknown Chapter')
    note_title = serializers.CharField(max_length=200, default='AI Generated Notes')
    note_content = serializers.CharField(default='No content available')
    note_type = serializers.CharField(max_length=50, default='ai_generated')
    
    def validate_class_name(self, value):
        if not value or value == 'undefined' or value == 'Class undefined':
            return 'Unknown Class'
        return value.strip()
    
    def validate_subject(self, value):
        if not value or value == 'undefined':
            return 'Unknown Subject'
        return value.strip()
    
    def validate_chapter(self, value):
        if not value or value == 'undefined':
            return 'Unknown Chapter'
        return value.strip()
    
    def validate_note_title(self, value):
        if not value or value == 'undefined':
            return 'AI Generated Notes'
        return value.strip()
    
    def validate_note_content(self, value):
        if not value or value == 'undefined':
            return 'No content available'
        return value.strip()
    
    class Meta:
        model = AIGeneratedNote
        fields = [
            'note_id', 'student_id', 'class_name', 'subject', 'chapter', 'subtopic',
            'note_title', 'note_content', 'note_type', 'key_points', 'summary',
            'is_favorite', 'created_at', 'updated_at'
        ]
        read_only_fields = ['note_id', 'created_at', 'updated_at']


class ManualNoteSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(max_length=50, default='Unknown Class')
    subject = serializers.CharField(max_length=100, default='Unknown Subject')
    chapter = serializers.CharField(max_length=200, default='Unknown Chapter')
    note_content = serializers.CharField(default='No content available')
    note_type = serializers.CharField(max_length=50, default='manual')
    color = serializers.CharField(max_length=7, default='#fef3c7')
    
    def validate_class_name(self, value):
        if not value or value == 'undefined' or value == 'Class undefined':
            return 'Unknown Class'
        return value.strip()
    
    def validate_subject(self, value):
        if not value or value == 'undefined':
            return 'Unknown Subject'
        return value.strip()
    
    def validate_chapter(self, value):
        if not value or value == 'undefined':
            return 'Unknown Chapter'
        return value.strip()
    
    def validate_note_content(self, value):
        if not value or value == 'undefined':
            return 'No content available'
        return value.strip()
    
    def validate_color(self, value):
        if not value or value == 'undefined':
            return '#fef3c7'
        return value.strip()
    
    class Meta:
        model = ManualNote
        fields = [
            'note_id', 'student_id', 'class_name', 'subject', 'chapter', 'subtopic',
            'note_title', 'note_content', 'note_type', 'color', 'is_important',
            'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['note_id', 'created_at', 'updated_at']


class AIChatHistorySerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(max_length=50, default='Unknown Class')
    subject = serializers.CharField(max_length=100, default='Unknown Subject')
    chapter = serializers.CharField(max_length=200, default='Unknown Chapter')
    user_message = serializers.CharField(default='No message')
    ai_response = serializers.CharField(default='No response')
    response_type = serializers.CharField(max_length=50, default='general')
    
    def validate_class_name(self, value):
        if not value or value == 'undefined' or value == 'Class undefined':
            return 'Unknown Class'
        return value.strip()
    
    def validate_subject(self, value):
        if not value or value == 'undefined':
            return 'Unknown Subject'
        return value.strip()
    
    def validate_chapter(self, value):
        if not value or value == 'undefined':
            return 'Unknown Chapter'
        return value.strip()
    
    def validate_user_message(self, value):
        if not value or value == 'undefined':
            return 'No message'
        return value.strip()
    
    def validate_ai_response(self, value):
        if not value or value == 'undefined':
            return 'No response'
        return value.strip()
    
    class Meta:
        model = AIChatHistory
        fields = [
            'chat_id', 'student_id', 'class_name', 'subject', 'chapter', 'subtopic',
            'user_message', 'ai_response', 'response_type', 'message_timestamp',
            'session_id', 'is_favorite'
        ]
        read_only_fields = ['chat_id', 'message_timestamp']


class AIInteractionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInteractionSession
        fields = [
            'session_id', 'student_id', 'class_name', 'subject', 'chapter', 'subtopic',
            'session_type', 'total_messages', 'started_at', 'ended_at', 'is_active'
        ]
        read_only_fields = ['started_at', 'ended_at']


class AIFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIFavorite
        fields = [
            'favorite_id', 'student_id', 'content_type', 'content_id',
            'favorite_title', 'created_at'
        ]
        read_only_fields = ['favorite_id', 'created_at']
