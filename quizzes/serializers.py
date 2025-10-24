from rest_framework import serializers
from .models import (
    Quiz, Question, QuestionOption, QuizAttempt, QuizAnswer,
    QuizResult, QuizAnalytics, StudentPerformance
)
from courses.serializers import SubjectSerializer
from authentication.serializers import UserSerializer


class QuestionOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for QuestionOption model
    """
    class Meta:
        model = QuestionOption
        fields = ['id', 'option_text', 'is_correct', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question model
    """
    options = QuestionOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'explanation',
            'points', 'order', 'is_active', 'options', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for Quiz model
    """
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    created_by = UserSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    attempts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'subject', 'subject_id', 'grade',
            'difficulty', 'duration_minutes', 'total_questions', 'passing_score',
            'is_published', 'is_premium', 'created_by', 'questions',
            'questions_count', 'attempts_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()
    
    def get_attempts_count(self, obj):
        return obj.attempts.count()


class QuizListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for quiz listing
    """
    subject = SubjectSerializer(read_only=True)
    questions_count = serializers.SerializerMethodField()
    attempts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'subject', 'grade',
            'difficulty', 'duration_minutes', 'passing_score',
            'is_premium', 'questions_count', 'attempts_count', 'created_at'
        ]
    
    def get_questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()
    
    def get_attempts_count(self, obj):
        return obj.attempts.count()


class QuizAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for QuizAnswer model
    """
    question = QuestionSerializer(read_only=True)
    selected_option = QuestionOptionSerializer(read_only=True)
    
    class Meta:
        model = QuizAnswer
        fields = [
            'id', 'question', 'selected_option', 'answer_text',
            'is_correct', 'points_earned', 'answered_at'
        ]
        read_only_fields = ['id', 'answered_at']


class QuizAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for QuizAttempt model
    """
    student = UserSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)
    answers = QuizAnswerSerializer(many=True, read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    quiz_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'student', 'student_id', 'quiz', 'quiz_id',
            'started_at', 'completed_at', 'time_taken_minutes',
            'score', 'is_completed', 'is_passed', 'answers'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at']


class QuizResultSerializer(serializers.ModelSerializer):
    """
    Serializer for QuizResult model
    """
    attempt = QuizAttemptSerializer(read_only=True)
    
    class Meta:
        model = QuizResult
        fields = [
            'id', 'attempt', 'total_questions', 'correct_answers',
            'wrong_answers', 'unanswered_questions', 'accuracy_percentage',
            'time_per_question_seconds', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class QuizAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for QuizAnalytics model
    """
    quiz = QuizSerializer(read_only=True)
    
    class Meta:
        model = QuizAnalytics
        fields = [
            'id', 'quiz', 'total_attempts', 'average_score',
            'pass_rate', 'average_time_minutes', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class QuizSubmissionSerializer(serializers.Serializer):
    """
    Serializer for quiz submission
    """
    quiz_id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.DictField()
    )
    
    def validate_answers(self, value):
        for answer in value:
            if 'question_id' not in answer:
                raise serializers.ValidationError("Each answer must have a question_id")
            if 'selected_option_id' not in answer and 'answer_text' not in answer:
                raise serializers.ValidationError("Each answer must have either selected_option_id or answer_text")
        return value


class QuizAttemptSummarySerializer(serializers.Serializer):
    """
    Serializer for quiz attempt summary
    """
    attempt_id = serializers.IntegerField()
    quiz_title = serializers.CharField()
    subject_name = serializers.CharField()
    score = serializers.FloatField()
    is_passed = serializers.BooleanField()
    time_taken_minutes = serializers.IntegerField()
    completed_at = serializers.DateTimeField()
    total_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()


class StudentQuizStatsSerializer(serializers.Serializer):
    """
    Serializer for student quiz statistics
    """
    total_quizzes_taken = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_correct_answers = serializers.IntegerField()
    total_questions_attempted = serializers.IntegerField()
    accuracy_percentage = serializers.FloatField()
    best_score = serializers.FloatField()
    quizzes_passed = serializers.IntegerField()
    total_quizzes_available = serializers.IntegerField()


class EnhancedQuizAttemptSerializer(serializers.ModelSerializer):
    """
    Enhanced serializer for QuizAttempt with AI-generated quiz support
    """
    student_name = serializers.CharField(source='student_id.firstname', read_only=True)
    student_username = serializers.CharField(source='student_id.username', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = [
            'attempt_id', 'quiz_id', 'student_id', 'student_name', 'student_username',
            'attempted_at', 'score', 'answers_json', 'quiz_type', 'subject', 'chapter',
            'topic', 'subtopic', 'class_name', 'difficulty_level', 'total_questions',
            'correct_answers', 'wrong_answers', 'unanswered_questions', 'time_taken_seconds',
            'completion_percentage', 'language', 'quiz_data_json'
        ]
        read_only_fields = ['attempt_id', 'attempted_at']


class QuizAttemptSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting quiz attempts (AI-generated quizzes)
    """
    # Quiz metadata - matches frontend data structure
    quizType = serializers.CharField(required=False, default='ai_generated')
    subject = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    chapter = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    topic = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    subtopic = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    className = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    difficultyLevel = serializers.ChoiceField(choices=['simple', 'medium', 'hard'], default='simple', required=False)
    language = serializers.CharField(max_length=10, default='English', required=False)
    
    # Quiz results - matches frontend data structure
    totalQuestions = serializers.IntegerField(required=False, default=0)
    correctAnswers = serializers.IntegerField(required=False, default=0)
    wrongAnswers = serializers.IntegerField(required=False, default=0)
    unansweredQuestions = serializers.IntegerField(required=False, default=0)
    timeTakenSeconds = serializers.IntegerField(required=False, default=0)
    score = serializers.FloatField(required=False, default=0.0)
    
    # Quiz data - matches frontend data structure
    quizQuestions = serializers.ListField(child=serializers.DictField(), required=False)
    userAnswers = serializers.ListField(child=serializers.CharField(), required=False)  # Changed to CharField for simple strings
    
    # Legacy fields for backward compatibility
    quiz_data_json = serializers.CharField(required=False, allow_blank=True)
    answers_json = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        # Map frontend field names to backend field names
        mapped_data = {
            'quiz_type': data.get('quizType', 'ai_generated'),
            'subject': data.get('subject'),
            'chapter': data.get('chapter', ''),
            'topic': data.get('topic', ''),
            'subtopic': data.get('subtopic'),
            'class_name': data.get('className'),
            'difficulty_level': data.get('difficultyLevel', 'simple'),
            'language': data.get('language', 'English'),
            'total_questions': data.get('totalQuestions'),
            'correct_answers': data.get('correctAnswers'),
            'wrong_answers': data.get('wrongAnswers'),
            'unanswered_questions': data.get('unansweredQuestions'),
            'time_taken_seconds': data.get('timeTakenSeconds'),
            'score': data.get('score'),
            'quiz_data_json': data.get('quiz_data_json', ''),
            'answers_json': data.get('answers_json', ''),
            'quiz_questions': data.get('quizQuestions', []),
            'user_answers': data.get('userAnswers', [])
        }
        
        # Validate that the numbers add up correctly
        total = mapped_data['correct_answers'] + mapped_data['wrong_answers'] + mapped_data['unanswered_questions']
        if total != mapped_data['total_questions']:
            raise serializers.ValidationError("Total questions must equal correct + wrong + unanswered")
        
        # Validate score is between 0 and 100
        if not 0 <= mapped_data['score'] <= 100:
            raise serializers.ValidationError("Score must be between 0 and 100")
        
        return mapped_data


class StudentPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentPerformance model
    """
    student_name = serializers.CharField(source='student.firstname', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    
    class Meta:
        model = StudentPerformance
        fields = [
            'student', 'student_name', 'student_username', 'total_quizzes_attempted',
            'total_questions_answered', 'total_correct_answers', 'overall_average_score',
            'mathematics_score', 'science_score', 'english_score', 'computers_score',
            'class_7_score', 'class_8_score', 'class_9_score', 'class_10_score',
            'simple_difficulty_score', 'medium_difficulty_score', 'hard_difficulty_score',
            'average_time_per_question', 'completion_rate', 'improvement_trend',
            'achievements_json', 'badges_earned', 'last_updated', 'last_quiz_date'
        ]
        read_only_fields = ['last_updated']


class RecentQuizAttemptsSerializer(serializers.ModelSerializer):
    """
    Serializer for recent quiz attempts (dashboard display)
    """
    subject_display = serializers.SerializerMethodField()
    difficulty_display = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    # Additional fields for frontend compatibility
    id = serializers.SerializerMethodField()
    class_name_display = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    score_percentage = serializers.SerializerMethodField()
    date_formatted = serializers.SerializerMethodField()
    quiz_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'attempt_id', 'quiz_type', 'subject', 'chapter', 'topic', 'subtopic', 'class_name',
            'difficulty_level', 'score', 'total_questions', 'correct_answers', 'wrong_answers',
            'time_taken_seconds', 'attempted_at', 'subject_display', 'difficulty_display', 'time_ago',
            'class_name_display', 'subject_name', 'topic_name', 'score_percentage', 'date_formatted', 'quiz_type_display'
        ]
    
    def get_subject_display(self, obj):
        return obj.subject or 'Unknown Subject'
    
    def get_difficulty_display(self, obj):
        return obj.difficulty_level.title() if obj.difficulty_level else 'Simple'
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        # Handle timezone-aware vs timezone-naive datetime comparison
        if obj.attempted_at:
            if timezone.is_aware(obj.attempted_at) and timezone.is_naive(now):
                now = timezone.make_aware(now)
            elif timezone.is_naive(obj.attempted_at) and timezone.is_aware(now):
                obj_time = timezone.make_aware(obj.attempted_at)
            else:
                obj_time = obj.attempted_at
            
            diff = now - obj_time
            
            if diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                return "Just now"
        else:
            return "Unknown"
    
    def get_id(self, obj):
        return obj.attempt_id
    
    def get_class_name_display(self, obj):
        return obj.class_name or 'Unknown Class'
    
    def get_subject_name(self, obj):
        return obj.subject or 'Unknown Subject'
    
    def get_topic_name(self, obj):
        return obj.subtopic or obj.topic or 'Unknown Topic'
    
    def get_score_percentage(self, obj):
        return round(obj.score, 1) if obj.score else 0
    
    def get_date_formatted(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        if not obj.attempted_at:
            return "Unknown"
            
        now = timezone.now()
        
        # Handle timezone-aware vs timezone-naive datetime comparison
        try:
            if timezone.is_aware(obj.attempted_at) and timezone.is_naive(now):
                now = timezone.make_aware(now)
            elif timezone.is_naive(obj.attempted_at) and timezone.is_aware(now):
                obj_time = timezone.make_aware(obj.attempted_at)
            else:
                obj_time = obj.attempted_at
            
            time_diff = now - obj_time
            
            if time_diff.days > 0:
                return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif time_diff.seconds > 60:
                minutes = time_diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                return "Just now"
        except:
            return obj.attempted_at.strftime('%Y-%m-%d %H:%M')
    
    def get_quiz_type_display(self, obj):
        if obj.quiz_type == 'ai_generated':
            return 'Quiz'
        elif obj.quiz_type == 'mock_test':
            return 'Mock Test'
        else:
            return 'Quiz'


class MockTestAttemptSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting mock test attempts
    """
    # Mock test metadata - matches frontend data structure
    testType = serializers.CharField(required=False, default='mock_test')
    subject = serializers.CharField(max_length=100)
    chapter = serializers.CharField(max_length=100, required=False, allow_blank=True)
    topic = serializers.CharField(max_length=200, required=False, allow_blank=True)
    subtopic = serializers.CharField(max_length=200)
    className = serializers.CharField(max_length=50)
    difficultyLevel = serializers.ChoiceField(choices=['simple', 'medium', 'hard'], default='simple')
    language = serializers.CharField(max_length=10, default='English')
    
    # Mock test results - matches frontend data structure
    totalQuestions = serializers.IntegerField()
    correctAnswers = serializers.IntegerField()
    wrongAnswers = serializers.IntegerField()
    unansweredQuestions = serializers.IntegerField()
    timeTakenSeconds = serializers.IntegerField()
    score = serializers.FloatField()
    
    # Mock test data - matches frontend data structure
    testQuestions = serializers.ListField(child=serializers.DictField(), required=False)
    userAnswers = serializers.ListField(child=serializers.CharField(), required=False)
    
    # Legacy fields for backward compatibility
    test_data_json = serializers.CharField(required=False, allow_blank=True)
    answers_json = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        # Map frontend field names to backend field names
        mapped_data = {
            'test_type': data.get('testType', 'mock_test'),
            'subject': data.get('subject'),
            'chapter': data.get('chapter', ''),
            'topic': data.get('topic', ''),
            'subtopic': data.get('subtopic'),
            'class_name': data.get('className'),
            'difficulty_level': data.get('difficultyLevel', 'simple'),
            'language': data.get('language', 'English'),
            'total_questions': data.get('totalQuestions'),
            'correct_answers': data.get('correctAnswers'),
            'wrong_answers': data.get('wrongAnswers'),
            'unanswered_questions': data.get('unansweredQuestions'),
            'time_taken_seconds': data.get('timeTakenSeconds'),
            'score': data.get('score'),
            'test_data_json': data.get('test_data_json', ''),
            'answers_json': data.get('answers_json', ''),
            'test_questions': data.get('testQuestions', []),
            'user_answers': data.get('userAnswers', [])
        }
        return mapped_data
