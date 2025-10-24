from django.db import models
from authentication.models import Class


class Course(models.Model):
    """
    Course model matching new schema
    """
    course_id = models.IntegerField(primary_key=True)
    class_id = models.IntegerField(null=True, blank=True)  # Changed from ForeignKey to IntegerField
    course_name = models.CharField(max_length=100)
    course_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.course_name
    
    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Topic(models.Model):
    """
    Topic model matching new schema
    """
    topic_id = models.AutoField(primary_key=True)
    course_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    topic_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.topic_name} - Course ID: {self.course_id}"
    
    class Meta:
        db_table = 'topic'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class PDFFiles(models.Model):
    """
    PDF Files model matching new schema with topic_id
    """
    pdf_id = models.AutoField(primary_key=True)
    course_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    topic_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    title = models.CharField(max_length=150)
    file_url = models.TextField()
    file_name = models.CharField(max_length=50)  # Added file_name
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size_in_kb = models.IntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - Course ID: {self.course_id}"
    
    class Meta:
        db_table = 'pdffiles'  # Updated table name to match schema
        verbose_name = 'PDF File'
        verbose_name_plural = 'PDF Files'


class VideoFiles(models.Model):
    """
    Video Files model matching new schema with topic_id
    """
    video_id = models.AutoField(primary_key=True)
    course_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    topic_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    title = models.CharField(max_length=150)
    file_url = models.TextField()
    file_name = models.CharField(max_length=50)  # Added file_name
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size_in_mb = models.IntegerField(null=True, blank=True)  # Changed to size_in_mb
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - Course ID: {self.course_id}"
    
    class Meta:
        db_table = 'videofiles'
        verbose_name = 'Video File'
        verbose_name_plural = 'Video Files'


# Legacy models for backward compatibility (if needed)
class Subject(models.Model):
    """
    Subject model for backward compatibility
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Chapter(models.Model):
    """
    Chapter model for backward compatibility
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    chapter_number = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.course_name} - {self.title}"
    
    class Meta:
        db_table = 'chapters'
        ordering = ['order']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'


class Lesson(models.Model):
    """
    Lesson model for backward compatibility
    """
    LESSON_TYPES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]
    
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='video')
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.chapter.title} - {self.title}"
    
    class Meta:
        db_table = 'lessons'
        ordering = ['order']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


class CourseEnrollment(models.Model):
    """
    Course enrollment model
    """
    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.course.course_name}"
    
    class Meta:
        db_table = 'course_enrollments'
        unique_together = ['student', 'course']
        verbose_name = 'Course Enrollment'
        verbose_name_plural = 'Course Enrollments'


class LessonProgress(models.Model):
    """
    Lesson progress tracking model
    """
    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completion_percentage = models.PositiveIntegerField(default=0)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.student_id.firstname} - {self.lesson.title}"
    
    class Meta:
        db_table = 'lesson_progress'
        unique_together = ['student', 'lesson']
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress'


class CourseMaterial(models.Model):
    """
    Course material model
    """
    MATERIAL_TYPES = [
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('link', 'Link'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    file_url = models.URLField(blank=True, null=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.course.course_name}"
    
    class Meta:
        db_table = 'course_materials'
        verbose_name = 'Course Material'
        verbose_name_plural = 'Course Materials'