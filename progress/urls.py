from django.urls import path
from . import views

urlpatterns = [
    # Attendance
    path('attendance/', views.AttendanceListCreateView.as_view(), name='attendance_list_create'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance_detail'),
    path('attendance/summary/', views.get_attendance_summary, name='attendance_summary'),
    
    # Assignments
    path('assignments/', views.AssignmentListCreateView.as_view(), name='assignment_list_create'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/<int:pk>/submit/', views.submit_assignment, name='assignment_submit'),
    path('my-assignments/', views.StudentAssignmentListView.as_view(), name='student_assignments'),
    
    # Grades
    path('grades/', views.GradeListCreateView.as_view(), name='grade_list_create'),
    path('grades/<int:pk>/', views.GradeDetailView.as_view(), name='grade_detail'),
    path('my-grades/', views.StudentGradeListView.as_view(), name='student_grades'),
    
    # Study Plans
    path('study-plans/', views.StudyPlanListCreateView.as_view(), name='study_plan_list_create'),
    path('study-plans/<int:pk>/', views.StudyPlanDetailView.as_view(), name='study_plan_detail'),
    path('study-plans/<int:pk>/items/', views.StudyPlanItemListCreateView.as_view(), name='study_plan_item_list_create'),
    path('study-plan-items/<int:pk>/', views.StudyPlanItemDetailView.as_view(), name='study_plan_item_detail'),
    path('study-plan-items/<int:pk>/complete/', views.complete_study_plan_item, name='complete_study_plan_item'),
    
    # Progress
    path('student-progress/', views.StudentProgressListCreateView.as_view(), name='student_progress_list_create'),
    path('student-progress/<int:pk>/', views.StudentProgressDetailView.as_view(), name='student_progress_detail'),
    path('my-progress/', views.get_my_progress, name='my_progress'),
    
    # Achievements
    path('achievements/', views.AchievementListCreateView.as_view(), name='achievement_list_create'),
    path('achievements/<int:pk>/', views.AchievementDetailView.as_view(), name='achievement_detail'),
    path('my-achievements/', views.MyAchievementsView.as_view(), name='my_achievements'),
    
    # Dashboard endpoints
    path('dashboard/', views.get_student_dashboard, name='student_dashboard'),
    path('parent-dashboard/', views.get_parent_dashboard, name='parent_dashboard'),
]
