from django.urls import path
from . import views
from . import static_quiz_views
from . import pdf_quiz_views

urlpatterns = [
    # Regular Quizzes (Database-based)
    path('', views.QuizListCreateView.as_view(), name='quiz_list_create'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('<int:pk>/start/', views.StartQuizView.as_view(), name='start_quiz'),
    path('<int:pk>/submit/', views.submit_quiz, name='submit_quiz'),
    
    # Questions
    path('<int:quiz_id>/questions/', views.QuestionListCreateView.as_view(), name='question_list_create'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    
    # Quiz Attempts
    path('attempts/', views.QuizAttemptListView.as_view(), name='quiz_attempt_list'),
    path('attempts/<int:pk>/', views.QuizAttemptDetailView.as_view(), name='quiz_attempt_detail'),
    path('attempts/<int:pk>/result/', views.get_quiz_result, name='quiz_result'),
    
    # Student specific endpoints
    path('my-attempts/', views.StudentQuizAttemptsView.as_view(), name='student_quiz_attempts'),
    path('stats/', views.get_student_quiz_stats, name='student_quiz_stats'),
    path('available/', views.AvailableQuizzesView.as_view(), name='available_quizzes'),
    
    # NEW: Enhanced Quiz Tracking System
    path('submit-attempt/', views.submit_quiz_attempt, name='submit_quiz_attempt'),
    path('submit-mock-test/', views.submit_mock_test_attempt, name='submit_mock_test_attempt'),
    path('recent-attempts/', views.get_recent_quiz_attempts, name='recent_quiz_attempts'),
    path('child-attempts/', views.get_child_quiz_attempts, name='child_quiz_attempts'),
    path('performance/', views.get_student_performance, name='student_performance'),
    path('statistics/', views.get_quiz_statistics, name='quiz_statistics'),
    
    # Static Quiz endpoints (7th Class Subjects)
    path('static/subjects/', static_quiz_views.get_static_subjects, name='static_subjects'),
    path('static/subjects/<str:subject>/topics/', static_quiz_views.get_static_topics, name='static_topics'),
    path('static/subjects/<str:subject>/topics/<str:topic>/', static_quiz_views.get_static_quiz, name='static_quiz'),
    path('static/subjects/<str:subject>/topics/<str:topic>/submit/', static_quiz_views.submit_static_quiz, name='static_quiz_submit'),
    path('static/subjects/<str:subject>/topics/<str:topic>/preview/', static_quiz_views.get_static_quiz_preview, name='static_quiz_preview'),
    path('static/statistics/', static_quiz_views.get_static_quiz_statistics, name='static_quiz_statistics'),
    path('static/help/', static_quiz_views.get_static_quiz_help, name='static_quiz_help'),
    
    # PDF Quiz endpoints (Serve PDF files organized by class/subject/topic/chapter)
    path('pdf/structure/', pdf_quiz_views.get_pdf_quiz_structure, name='pdf_quiz_structure'),
    path('pdf/<str:class_name>/subjects/', pdf_quiz_views.get_pdf_quiz_subjects, name='pdf_quiz_subjects'),
    path('pdf/<str:class_name>/<str:subject>/topics/', pdf_quiz_views.get_pdf_quiz_topics, name='pdf_quiz_topics'),
    path('pdf/<str:class_name>/<str:subject>/<str:topic>/info/', pdf_quiz_views.get_pdf_quiz_info, name='pdf_quiz_info'),
    path('pdf/<str:class_name>/<str:subject>/<str:topic>/download/', pdf_quiz_views.download_pdf_quiz, name='pdf_quiz_download'),
    path('pdf/<str:class_name>/<str:subject>/<str:topic>/', pdf_quiz_views.get_pdf_quiz_for_frontend, name='pdf_quiz_frontend'),
    path('pdf/search/', pdf_quiz_views.search_pdf_quizzes, name='pdf_quiz_search'),
    path('pdf/statistics/', pdf_quiz_views.get_pdf_quiz_statistics, name='pdf_quiz_statistics'),
    
    # Interactive PDF Quiz endpoints (Extract questions from PDFs and make them interactive)
    path('pdf/<str:class_name>/<str:subject>/<str:topic_key>/questions/', pdf_quiz_views.get_pdf_quiz_questions, name='pdf_quiz_questions'),
    path('pdf/<str:class_name>/<str:subject>/<str:topic_key>/submit/', pdf_quiz_views.submit_pdf_quiz_answers, name='pdf_quiz_submit'),
    
    # Randomized Maths Quiz endpoints (10 random questions from full question bank)
    path('maths/<str:class_name>/<str:subject>/<str:topic_key>/randomized/', pdf_quiz_views.get_maths_randomized_quiz, name='maths_randomized_quiz'),
    path('maths/<str:class_name>/<str:subject>/<str:topic_key>/randomized/submit/', pdf_quiz_views.submit_maths_randomized_quiz_answers, name='maths_randomized_quiz_submit'),
]
