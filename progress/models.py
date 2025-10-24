from django.db import models
from authentication.models import User, Student, StudentRegistration
from courses.models import Course, Topic


class Assignment(models.Model):
    """
    Assignment model matching new schema
    """
    assignment_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField()
    due_date = models.DateField()
    file_url = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.description[:50]}... - {self.topic_id.topic_name}"
    
    class Meta:
        db_table = 'assignments'  # Updated table name to match schema
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'


class AssignmentQuestion(models.Model):
    """
    Assignment Question model matching new schema
    """
    question_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1)
    
    def __str__(self):
        return f"{self.question_text[:50]}... - {self.assignment_id.description[:30]}..."
    
    class Meta:
        db_table = 'assignment_question'  # Updated table name to match schema
        verbose_name = 'Assignment Question'
        verbose_name_plural = 'Assignment Questions'


class AssignmentSubmission(models.Model):
    """
    Assignment Submission model matching new schema
    """
    submission_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_id = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE)  # Updated to use StudentRegistration
    submitted_at = models.DateTimeField(auto_now_add=True)
    file_url = models.TextField(null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_id.first_name} - {self.assignment_id.description[:30]}..."
    
    class Meta:
        db_table = 'assignment_submission'  # Updated table name to match schema
        verbose_name = 'Assignment Submission'
        verbose_name_plural = 'Assignment Submissions'


class AssignmentAnswer(models.Model):
    """
    Assignment Answer model matching new schema
    """
    answer_id = models.AutoField(primary_key=True)
    submission_id = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE, related_name='answers')
    question_id = models.ForeignKey(AssignmentQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    
    def __str__(self):
        return f"{self.submission_id.student_id.first_name} - Q{self.question_id.question_id}"
    
    class Meta:
        db_table = 'assignment_answer'  # Updated table name to match schema
        verbose_name = 'Assignment Answer'
        verbose_name_plural = 'Assignment Answers'


class CareerPerformance(models.Model):
    """
    Career Performance model matching existing schema
    """
    performance_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    avg_assignment_score = models.FloatField(null=True, blank=True)
    avg_mocktest_score = models.FloatField(null=True, blank=True)
    overall_rating = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student_id.student_id.firstname} - Performance"
    
    class Meta:
        db_table = 'careerperformance'
        verbose_name = 'Career Performance'
        verbose_name_plural = 'Career Performances'


class MentorshipTicket(models.Model):
    """
    Mentorship Ticket model matching existing schema
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    ticket_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructor_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.student_id.student_id.firstname}"
    
    class Meta:
        db_table = 'mentorshipticket'
        verbose_name = 'Mentorship Ticket'
        verbose_name_plural = 'Mentorship Tickets'


# Legacy models for backward compatibility (if needed)
class Attendance(models.Model):
    """
    Attendance model for backward compatibility
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.date} - {self.status}"
    
    class Meta:
        db_table = 'attendance'
        unique_together = ['student', 'course', 'date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'


class Grade(models.Model):
    """
    Grade model for backward compatibility
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    grade_value = models.FloatField()
    max_grade = models.FloatField(default=100)
    grade_type = models.CharField(max_length=50, default='assignment')
    comments = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    graded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.grade_value}/{self.max_grade}"
    
    class Meta:
        db_table = 'grades'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'


class StudentProgress(models.Model):
    """
    Student Progress model for backward compatibility
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    overall_percentage = models.FloatField(default=0)
    lessons_completed = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=0)
    assignments_completed = models.PositiveIntegerField(default=0)
    total_assignments = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.course.course_name} - {self.overall_percentage}%"
    
    class Meta:
        db_table = 'student_progress'
        unique_together = ['student', 'course']
        verbose_name = 'Student Progress'
        verbose_name_plural = 'Student Progress'


class StudyPlan(models.Model):
    """
    Study Plan model for backward compatibility
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.title}"
    
    class Meta:
        db_table = 'study_plans'
        verbose_name = 'Study Plan'
        verbose_name_plural = 'Study Plans'


class StudyPlanItem(models.Model):
    """
    Study Plan Item model for backward compatibility
    """
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.study_plan.title} - {self.title}"
    
    class Meta:
        db_table = 'study_plan_items'
        ordering = ['order']
        verbose_name = 'Study Plan Item'
        verbose_name_plural = 'Study Plan Items'


class Achievement(models.Model):
    """
    Achievement model for backward compatibility
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(max_length=50)
    points = models.PositiveIntegerField(default=0)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.title}"
    
    class Meta:
        db_table = 'achievements'
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'