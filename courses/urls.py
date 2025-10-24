from django.urls import path
from . import views

urlpatterns = [
    # Subjects
    path('subjects/', views.SubjectListCreateView.as_view(), name='subject_list_create'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    
    # Courses
    path('', views.CourseListCreateView.as_view(), name='course_list_create'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', views.CourseEnrollmentView.as_view(), name='course_enroll'),
    path('<int:pk>/progress/', views.get_course_progress, name='course_progress'),
    
    # Chapters
    path('<int:course_id>/chapters/', views.ChapterListCreateView.as_view(), name='chapter_list_create'),
    path('chapters/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter_detail'),
    
    # Lessons
    path('chapters/<int:chapter_id>/lessons/', views.LessonListCreateView.as_view(), name='lesson_list_create'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/progress/', views.update_lesson_progress, name='lesson_progress'),
    
    # Materials
    path('<int:course_id>/materials/', views.CourseMaterialListCreateView.as_view(), name='material_list_create'),
    path('materials/<int:pk>/', views.CourseMaterialDetailView.as_view(), name='material_detail'),
    
    # Student specific endpoints
    path('my-courses/', views.StudentCourseListView.as_view(), name='student_courses'),
    path('my-progress/', views.get_student_progress, name='student_progress'),
]
