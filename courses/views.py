from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from django.utils import timezone

from .models import (
    Subject, Course, Chapter, Lesson, CourseEnrollment,
    LessonProgress, CourseMaterial
)
from .serializers import (
    SubjectSerializer, CourseSerializer, ChapterSerializer, LessonSerializer,
    CourseEnrollmentSerializer, LessonProgressSerializer, CourseMaterialSerializer,
    CourseListSerializer, CourseDetailSerializer, StudentCourseProgressSerializer
)


class SubjectListCreateView(generics.ListCreateAPIView):
    """
    List and create subjects
    """
    queryset = Subject.objects.filter(is_active=True)
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a subject
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseListCreateView(generics.ListCreateAPIView):
    """
    List and create courses
    """
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        grade = self.request.query_params.get('grade')
        subject_id = self.request.query_params.get('subject')
        
        if grade:
            queryset = queryset.filter(grade=grade)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        return queryset


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a course
    """
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChapterListCreateView(generics.ListCreateAPIView):
    """
    List and create chapters for a course
    """
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Chapter.objects.filter(course_id=course_id, is_published=True)
    
    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        serializer.save(course_id=course_id)


class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a chapter
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonListCreateView(generics.ListCreateAPIView):
    """
    List and create lessons for a chapter
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return Lesson.objects.filter(chapter_id=chapter_id, is_published=True)
    
    def perform_create(self, serializer):
        chapter_id = self.kwargs['chapter_id']
        serializer.save(chapter_id=chapter_id)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a lesson
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseMaterialListCreateView(generics.ListCreateAPIView):
    """
    List and create course materials
    """
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return CourseMaterial.objects.filter(course_id=course_id)


class CourseMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete course material
    """
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseEnrollmentView(generics.CreateAPIView):
    """
    Enroll in a course
    """
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        course_id = self.kwargs['pk']
        serializer.save(
            student=self.request.user,
            course_id=course_id,
            enrolled_at=timezone.now()
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_course_progress(request, pk):
    """
    Get course progress for a student
    """
    try:
        enrollment = CourseEnrollment.objects.get(
            student=request.user,
            course_id=pk,
            is_active=True
        )
        
        # Get lesson progress
        lessons = Lesson.objects.filter(
            chapter__course_id=pk,
            is_published=True
        )
        
        lesson_progress = LessonProgress.objects.filter(
            student=request.user,
            lesson__in=lessons
        )
        
        total_lessons = lessons.count()
        completed_lessons = lesson_progress.filter(is_completed=True).count()
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        return Response({
            'course_id': pk,
            'enrollment_date': enrollment.enrolled_at,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percentage': progress_percentage,
            'last_accessed': enrollment.last_accessed
        })
    
    except CourseEnrollment.DoesNotExist:
        return Response(
            {'error': 'Not enrolled in this course'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_lesson_progress(request, pk):
    """
    Update lesson progress
    """
    try:
        lesson = Lesson.objects.get(pk=pk)
        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson
        )
        
        completion_percentage = request.data.get('completion_percentage', 0)
        time_spent = request.data.get('time_spent_minutes', 0)
        
        progress.completion_percentage = completion_percentage
        progress.time_spent_minutes += time_spent
        progress.last_accessed = timezone.now()
        
        if completion_percentage >= 100:
            progress.is_completed = True
            progress.completed_at = timezone.now()
        
        progress.save()
        
        return Response({
            'message': 'Progress updated successfully',
            'progress': LessonProgressSerializer(progress).data
        })
    
    except Lesson.DoesNotExist:
        return Response(
            {'error': 'Lesson not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class StudentCourseListView(generics.ListAPIView):
    """
    Get student's enrolled courses
    """
    serializer_class = StudentCourseProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        enrollments = CourseEnrollment.objects.filter(
            student=self.request.user,
            is_active=True
        )
        
        course_data = []
        for enrollment in enrollments:
            course = enrollment.course
            lessons = Lesson.objects.filter(
                chapter__course=course,
                is_published=True
            )
            lesson_progress = LessonProgress.objects.filter(
                student=self.request.user,
                lesson__in=lessons
            )
            
            total_lessons = lessons.count()
            completed_lessons = lesson_progress.filter(is_completed=True).count()
            progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
            
            course_data.append({
                'course_id': course.id,
                'course_title': course.title,
                'subject_name': course.subject.name,
                'total_lessons': total_lessons,
                'completed_lessons': completed_lessons,
                'progress_percentage': progress_percentage,
                'last_accessed': enrollment.last_accessed,
                'enrollment_date': enrollment.enrolled_at
            })
        
        return course_data


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_progress(request):
    """
    Get overall student progress
    """
    user = request.user
    
    # Get all enrollments
    enrollments = CourseEnrollment.objects.filter(student=user, is_active=True)
    
    # Calculate overall progress
    total_courses = enrollments.count()
    total_progress = 0
    
    for enrollment in enrollments:
        lessons = Lesson.objects.filter(
            chapter__course=enrollment.course,
            is_published=True
        )
        lesson_progress = LessonProgress.objects.filter(
            student=user,
            lesson__in=lessons
        )
        
        total_lessons = lessons.count()
        completed_lessons = lesson_progress.filter(is_completed=True).count()
        course_progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        total_progress += course_progress
    
    overall_progress = total_progress / total_courses if total_courses > 0 else 0
    
    return Response({
        'total_courses': total_courses,
        'overall_progress': overall_progress,
        'courses': StudentCourseListView().get_queryset()
    })
