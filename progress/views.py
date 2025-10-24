from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    Attendance, Assignment, AssignmentSubmission, Grade, StudyPlan,
    StudyPlanItem, StudentProgress, Achievement
)
from .serializers import (
    AttendanceSerializer, AssignmentSerializer, AssignmentSubmissionSerializer,
    GradeSerializer, StudyPlanSerializer, StudyPlanItemSerializer,
    StudentProgressSerializer, AchievementSerializer, AttendanceSummarySerializer,
    StudentDashboardSerializer, ParentDashboardSerializer
)


class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    List and create attendance records
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student')
        subject_id = self.request.query_params.get('subject')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete attendance record
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_attendance_summary(request):
    """
    Get attendance summary for a student
    """
    student_id = request.query_params.get('student', request.user.id)
    
    # Get attendance records grouped by subject
    attendance_records = Attendance.objects.filter(student_id=student_id)
    
    summary_data = []
    subjects = set([record.subject for record in attendance_records])
    
    for subject in subjects:
        subject_records = attendance_records.filter(subject=subject)
        total_days = subject_records.count()
        present_days = subject_records.filter(status='present').count()
        absent_days = subject_records.filter(status='absent').count()
        late_days = subject_records.filter(status='late').count()
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        summary_data.append({
            'subject_name': subject.name,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'attendance_percentage': attendance_percentage
        })
    
    return Response(summary_data)


class AssignmentListCreateView(generics.ListCreateAPIView):
    """
    List and create assignments
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        subject_id = self.request.query_params.get('subject')
        assigned_to = self.request.query_params.get('assigned_to')
        
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        
        return queryset


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete assignment
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_assignment(request, pk):
    """
    Submit assignment
    """
    try:
        assignment = Assignment.objects.get(pk=pk)
        
        # Check if student is assigned to this assignment
        if request.user not in assignment.assigned_to.all():
            return Response(
                {'error': 'You are not assigned to this assignment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already submitted
        existing_submission = AssignmentSubmission.objects.filter(
            assignment=assignment,
            student=request.user
        ).first()
        
        if existing_submission:
            return Response(
                {'error': 'Assignment already submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create submission
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=request.user,
            submission_text=request.data.get('submission_text', ''),
            submission_file=request.FILES.get('submission_file')
        )
        
        return Response({
            'message': 'Assignment submitted successfully',
            'submission': AssignmentSubmissionSerializer(submission).data
        })
    
    except Assignment.DoesNotExist:
        return Response(
            {'error': 'Assignment not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class StudentAssignmentListView(generics.ListAPIView):
    """
    Get student's assignments
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Assignment.objects.filter(
            assigned_to=self.request.user,
            is_published=True
        ).order_by('-created_at')


class GradeListCreateView(generics.ListCreateAPIView):
    """
    List and create grades
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student')
        subject_id = self.request.query_params.get('subject')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        return queryset


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete grade
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentGradeListView(generics.ListAPIView):
    """
    Get student's grades
    """
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Grade.objects.filter(student=self.request.user).order_by('-graded_at')


class StudyPlanListCreateView(generics.ListCreateAPIView):
    """
    List and create study plans
    """
    queryset = StudyPlan.objects.all()
    serializer_class = StudyPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return StudyPlan.objects.filter(student=self.request.user)


class StudyPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete study plan
    """
    queryset = StudyPlan.objects.all()
    serializer_class = StudyPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudyPlanItemListCreateView(generics.ListCreateAPIView):
    """
    List and create study plan items
    """
    serializer_class = StudyPlanItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        study_plan_id = self.kwargs['pk']
        return StudyPlanItem.objects.filter(study_plan_id=study_plan_id)
    
    def perform_create(self, serializer):
        study_plan_id = self.kwargs['pk']
        serializer.save(study_plan_id=study_plan_id)


class StudyPlanItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete study plan item
    """
    queryset = StudyPlanItem.objects.all()
    serializer_class = StudyPlanItemSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_study_plan_item(request, pk):
    """
    Mark study plan item as completed
    """
    try:
        item = StudyPlanItem.objects.get(pk=pk)
        item.is_completed = True
        item.completed_at = timezone.now()
        item.save()
        
        return Response({
            'message': 'Study plan item completed successfully',
            'item': StudyPlanItemSerializer(item).data
        })
    
    except StudyPlanItem.DoesNotExist:
        return Response(
            {'error': 'Study plan item not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class StudentProgressListCreateView(generics.ListCreateAPIView):
    """
    List and create student progress records
    """
    queryset = StudentProgress.objects.all()
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset


class StudentProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete student progress record
    """
    queryset = StudentProgress.objects.all()
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_progress(request):
    """
    Get current user's progress
    """
    progress_records = StudentProgress.objects.filter(student=request.user)
    
    overall_progress = 0
    if progress_records.exists():
        overall_progress = sum([p.overall_percentage for p in progress_records]) / progress_records.count()
    
    return Response({
        'overall_progress': overall_progress,
        'subjects': StudentProgressSerializer(progress_records, many=True).data
    })


class AchievementListCreateView(generics.ListCreateAPIView):
    """
    List and create achievements
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete achievement
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyAchievementsView(generics.ListAPIView):
    """
    Get current user's achievements
    """
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Achievement.objects.filter(student=self.request.user).order_by('-earned_at')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_dashboard(request):
    """
    Get student dashboard data
    """
    user = request.user
    
    # Get progress data
    progress_records = StudentProgress.objects.filter(student=user)
    overall_progress = sum([p.overall_percentage for p in progress_records]) / len(progress_records) if progress_records else 0
    
    # Get assignments
    assignments = Assignment.objects.filter(assigned_to=user)
    pending_assignments = assignments.filter(due_date__gt=timezone.now())
    completed_assignments = AssignmentSubmission.objects.filter(student=user).count()
    
    # Get quiz data
    from quizzes.models import QuizAttempt
    quiz_attempts = QuizAttempt.objects.filter(student=user, is_completed=True)
    average_quiz_score = quiz_attempts.aggregate(avg_score=Avg('score'))['avg_score'] or 0
    
    # Get attendance
    attendance_records = Attendance.objects.filter(student=user)
    attendance_percentage = 0
    if attendance_records.exists():
        present_days = attendance_records.filter(status='present').count()
        total_days = attendance_records.count()
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    # Get recent achievements
    recent_achievements = Achievement.objects.filter(student=user).order_by('-earned_at')[:5]
    
    # Get upcoming assignments
    upcoming_assignments = assignments.filter(
        due_date__gt=timezone.now(),
        due_date__lte=timezone.now() + timedelta(days=7)
    ).order_by('due_date')[:5]
    
    # Get study plans
    study_plans = StudyPlan.objects.filter(student=user, is_active=True)
    
    dashboard_data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role
        },
        'overall_progress': overall_progress,
        'active_courses': progress_records.count(),
        'completed_assignments': completed_assignments,
        'pending_assignments': pending_assignments.count(),
        'quizzes_taken': quiz_attempts.count(),
        'average_quiz_score': average_quiz_score,
        'attendance_percentage': attendance_percentage,
        'recent_achievements': AchievementSerializer(recent_achievements, many=True).data,
        'upcoming_assignments': AssignmentSerializer(upcoming_assignments, many=True).data,
        'study_plans': StudyPlanSerializer(study_plans, many=True).data
    }
    
    return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_parent_dashboard(request):
    """
    Get parent dashboard data
    """
    user = request.user
    
    # Get children using new schema
    from authentication.models import StudentRegistration, StudentProfile
    children = StudentRegistration.objects.filter(parent_email=user.email)
    
    children_data = []
    for child in children:
        try:
            # Get child's profile
            profile = StudentProfile.objects.get(student_id=child.student_id)
            
            # Get child's progress (if any)
            progress_records = StudentProgress.objects.filter(student_id=child.student_id)
            overall_progress = sum([p.overall_percentage for p in progress_records]) / len(progress_records) if progress_records else 0
            
            # Get attendance (if any)
            attendance_records = Attendance.objects.filter(student_id=child.student_id)
            attendance_percentage = 0
            if attendance_records.exists():
                present_days = attendance_records.filter(status='present').count()
                total_days = attendance_records.count()
                attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
            
            children_data.append({
                'child': {
                    'id': child.student_id,
                    'username': child.student_username,
                    'first_name': child.first_name,
                    'last_name': child.last_name,
                    'email': child.student_email,
                    'grade': profile.grade if profile else 'N/A',
                    'school': profile.school if profile else 'N/A'
                },
                'overall_progress': overall_progress,
                'attendance_percentage': attendance_percentage,
                'subjects_count': progress_records.count()
            })
        except StudentProfile.DoesNotExist:
            # If no profile exists, still include basic child data
            children_data.append({
                'child': {
                    'id': child.student_id,
                    'username': child.student_username,
                    'first_name': child.first_name,
                    'last_name': child.last_name,
                    'email': child.student_email,
                    'grade': 'N/A',
                    'school': 'N/A'
                },
                'overall_progress': 0,
                'attendance_percentage': 0,
                'subjects_count': 0
            })
    
    # Get recent notifications (you can implement this based on your notification system)
    recent_notifications = []
    
    # Get upcoming events (you can implement this based on your event system)
    upcoming_events = []
    
    dashboard_data = {
        'user': {
            'id': user.userid,
            'username': user.username,
            'first_name': user.firstname,
            'last_name': user.lastname,
            'role': user.role
        },
        'children': [child_data['child'] for child_data in children_data],
        'children_progress': children_data,
        'recent_notifications': recent_notifications,
        'upcoming_events': upcoming_events
    }
    
    return Response(dashboard_data)
