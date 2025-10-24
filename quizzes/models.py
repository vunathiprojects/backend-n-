from django.db import models
from authentication.models import User, Student, StudentRegistration
from courses.models import Topic


class Quiz(models.Model):
    """
    Quiz model matching actual database schema
    """
    quiz_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, db_column='topic_id')
    title = models.CharField(max_length=150, null=True, blank=True)
    questions_json = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title or 'Untitled Quiz'} - {self.topic_id.topic_name if self.topic_id else 'No Topic'}"
    
    class Meta:
        db_table = 'quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'


class QuizQuestion(models.Model):
    """
    Quiz Question model matching new schema
    """
    question_id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quiz_id')
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    
    def __str__(self):
        return f"Q{self.question_id}: {self.question_text[:50]}..."
    
    class Meta:
        db_table = 'quiz_question'
        verbose_name = 'Quiz Question'
        verbose_name_plural = 'Quiz Questions'


class QuizAttempt(models.Model):
    """
    Quiz Attempt model with enhanced tracking for AI-generated quizzes
    """
    attempt_id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True, db_column='quiz_id')  # Can be null for AI-generated quizzes
    student_id = models.ForeignKey('authentication.StudentRegistration', on_delete=models.CASCADE, db_column='student_id')
    attempted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    answers_json = models.TextField(null=True, blank=True)
    
    # Enhanced tracking fields for AI-generated quizzes
    quiz_type = models.CharField(max_length=20, choices=[
        ('database', 'Database Quiz'),
        ('ai_generated', 'AI Generated Quiz'),
        ('mock_test', 'Mock Test'),
    ], default='ai_generated')
    
    # Subject and topic information
    subject = models.CharField(max_length=100, null=True, blank=True)
    chapter = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=200, null=True, blank=True)
    subtopic = models.CharField(max_length=200, null=True, blank=True)
    
    # Class and difficulty information
    class_name = models.CharField(max_length=50, null=True, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('simple', 'Simple'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='simple')
    
    # Quiz details
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    wrong_answers = models.PositiveIntegerField(default=0)
    unanswered_questions = models.PositiveIntegerField(default=0)
    
    # Time tracking
    time_taken_seconds = models.PositiveIntegerField(default=0)
    completion_percentage = models.FloatField(default=0.0)
    
    # Language and metadata
    language = models.CharField(max_length=10, default='English')
    quiz_data_json = models.TextField(null=True, blank=True)  # Store the full quiz data
    
    def __str__(self):
        return f"{self.student_id.firstname} - {self.topic or self.quiz_id.title if self.quiz_id else 'AI Quiz'}"
    
    class Meta:
        db_table = 'quiz_attempt'
        verbose_name = 'Quiz Attempt'
        verbose_name_plural = 'Quiz Attempts'
        ordering = ['-attempted_at']


class QuizAnswer(models.Model):
    """
    Quiz Answer model matching new schema
    """
    answer_id = models.AutoField(primary_key=True)
    attempt_id = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, db_column='attempt_id')
    question_id = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, db_column='question_id')
    selected_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    is_correct = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"Answer {self.answer_id}: {self.selected_option} ({'Correct' if self.is_correct else 'Incorrect'})"
    
    class Meta:
        db_table = 'quiz_answer'
        verbose_name = 'Quiz Answer'
        verbose_name_plural = 'Quiz Answers'


class MockTest(models.Model):
    """
    Mock Test model matching provided schema
    """
    test_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, db_column='topic_id')
    title = models.CharField(max_length=150)
    total_marks = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # in minutes
    
    def __str__(self):
        return f"{self.title} - {self.topic_id.topic_name if self.topic_id else 'No Topic'}"
    
    class Meta:
        db_table = 'mock_test'
        verbose_name = 'Mock Test'
        verbose_name_plural = 'Mock Tests'


class MockTestQuestion(models.Model):
    """
    Mock Test Question model matching new schema
    """
    question_id = models.AutoField(primary_key=True)
    test_id = models.ForeignKey(MockTest, on_delete=models.CASCADE, db_column='test_id')
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    
    def __str__(self):
        return f"MT Q{self.question_id}: {self.question_text[:50]}..."
    
    class Meta:
        db_table = 'mock_test_question'
        verbose_name = 'Mock Test Question'
        verbose_name_plural = 'Mock Test Questions'


class MockTestAttempt(models.Model):
    """
    Mock Test Attempt model matching quiz_attempt schema
    """
    attempt_id = models.AutoField(primary_key=True)
    test_id = models.ForeignKey(MockTest, on_delete=models.CASCADE, db_column='test_id')
    student_id = models.ForeignKey('authentication.StudentRegistration', on_delete=models.CASCADE, db_column='student_id')
    attempted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    
    # Additional fields to match quiz_attempt table
    answers_json = models.TextField(null=True, blank=True)
    quiz_type = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    chapter = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    subtopic = models.CharField(max_length=100, null=True, blank=True)
    class_name = models.CharField(max_length=50, null=True, blank=True)
    difficulty_level = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    total_questions = models.IntegerField(null=True, blank=True)
    correct_answers = models.IntegerField(null=True, blank=True)
    wrong_answers = models.IntegerField(null=True, blank=True)
    unanswered_questions = models.IntegerField(null=True, blank=True)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    completion_percentage = models.FloatField(null=True, blank=True)
    mock_test_data_json = models.TextField(null=True, blank=True, db_column='mock_test_data_json')
    
    def __str__(self):
        return f"{self.student_id.firstname} - {self.test_id.title if self.test_id else 'Mock Test'}"
    
    class Meta:
        db_table = 'mock_test_attempt'
        verbose_name = 'Mock Test Attempt'
        verbose_name_plural = 'Mock Test Attempts'
        ordering = ['-attempted_at']


class MockTestAnswer(models.Model):
    """
    Mock Test Answer model matching new schema
    """
    answer_id = models.AutoField(primary_key=True)
    attempt_id = models.ForeignKey(MockTestAttempt, on_delete=models.CASCADE, db_column='attempt_id')
    question_id = models.ForeignKey(MockTestQuestion, on_delete=models.CASCADE, db_column='question_id')
    selected_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    is_correct = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"Answer {self.answer_id}: {self.selected_option} ({'Correct' if self.is_correct else 'Incorrect'})"
    
    class Meta:
        db_table = 'mock_test_answer'
        verbose_name = 'Mock Test Answer'
        verbose_name_plural = 'Mock Test Answers'


# Legacy models for backward compatibility (if needed)
class Question(models.Model):
    """
    Question model for backward compatibility
    """
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('text', 'Text Answer'),
        ('numeric', 'Numeric Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"
    
    class Meta:
        db_table = 'questions'
        ordering = ['order']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class QuestionOption(models.Model):
    """
    Question Option model for backward compatibility
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.question_text[:50]}... - {self.option_text[:30]}..."
    
    class Meta:
        db_table = 'question_options'
        ordering = ['order']
        verbose_name = 'Question Option'
        verbose_name_plural = 'Question Options'


class LegacyQuizAnswer(models.Model):
    """
    Legacy Quiz Answer model for backward compatibility
    """
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='legacy_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, null=True, blank=True)
    answer_text = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.attempt.student_id.firstname if self.attempt.student_id else 'Unknown'} - {self.question.question_text[:30] if self.question else 'Unknown'}..."
    
    class Meta:
        db_table = 'legacy_quiz_answers'
        unique_together = ['attempt', 'question']
        verbose_name = 'Legacy Quiz Answer'
        verbose_name_plural = 'Legacy Quiz Answers'


class QuizResult(models.Model):
    """
    Quiz Result model for detailed analytics
    """
    attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='result')
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    wrong_answers = models.PositiveIntegerField()
    unanswered_questions = models.PositiveIntegerField(default=0)
    accuracy_percentage = models.FloatField()
    time_per_question_seconds = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.attempt.student_id.firstname} - {self.accuracy_percentage}%"
    
    class Meta:
        db_table = 'quiz_results'
        verbose_name = 'Quiz Result'
        verbose_name_plural = 'Quiz Results'


class QuizAnalytics(models.Model):
    """
    Quiz Analytics model for aggregate statistics
    """
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name='analytics')
    total_attempts = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0)
    pass_rate = models.FloatField(default=0)
    average_time_minutes = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Analytics"
    
    class Meta:
        db_table = 'quiz_analytics'
        verbose_name = 'Quiz Analytics'
        verbose_name_plural = 'Quiz Analytics'


class StudentPerformance(models.Model):
    """
    Student Performance model for tracking overall student progress
    """
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='performance')
    
    # Overall statistics
    total_quizzes_attempted = models.PositiveIntegerField(default=0)
    total_questions_answered = models.PositiveIntegerField(default=0)
    total_correct_answers = models.PositiveIntegerField(default=0)
    overall_average_score = models.FloatField(default=0.0)
    
    # Subject-wise performance
    mathematics_score = models.FloatField(default=0.0)
    science_score = models.FloatField(default=0.0)
    english_score = models.FloatField(default=0.0)
    computers_score = models.FloatField(default=0.0)
    
    # Class-wise performance
    class_7_score = models.FloatField(default=0.0)
    class_8_score = models.FloatField(default=0.0)
    class_9_score = models.FloatField(default=0.0)
    class_10_score = models.FloatField(default=0.0)
    
    # Difficulty-wise performance
    simple_difficulty_score = models.FloatField(default=0.0)
    medium_difficulty_score = models.FloatField(default=0.0)
    hard_difficulty_score = models.FloatField(default=0.0)
    
    # Time and consistency
    average_time_per_question = models.FloatField(default=0.0)
    completion_rate = models.FloatField(default=0.0)
    improvement_trend = models.FloatField(default=0.0)  # Positive/negative trend
    
    # Achievements and badges
    achievements_json = models.TextField(null=True, blank=True)  # Store achievements as JSON
    badges_earned = models.PositiveIntegerField(default=0)
    
    # Last updated
    last_updated = models.DateTimeField(auto_now=True)
    last_quiz_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.firstname} - Performance"
    
    class Meta:
        db_table = 'student_performance'
        verbose_name = 'Student Performance'
        verbose_name_plural = 'Student Performances'