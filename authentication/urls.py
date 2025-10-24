from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    
    # Password management
    path('change-password/', views.change_password, name='change_password'),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('confirm-password-reset/', views.confirm_password_reset, name='confirm_password_reset'),
    
    # Profile management
    path('profile/', views.get_user_profile, name='get_profile'),
    path('profile/data/', views.get_user_profile_data, name='get_profile_data'),
    path('profile/update/', views.update_user_profile, name='update_profile'),
    path('dashboard/', views.get_dashboard_data, name='dashboard'),
    
    # Role-specific endpoints
    path('students/', views.StudentListCreateView.as_view(), name='student_list_create'),
    path('parents/', views.ParentListCreateView.as_view(), name='parent_list_create'),
    
    # New schema endpoints
    path('register-parent/', views.register_parent, name='register_parent'),
    path('register-student/', views.register_student, name='register_student'),
    path('parents-list/', views.get_parents, name='get_parents'),
    path('students-list/', views.get_students, name='get_students'),
    path('student/<int:student_id>/', views.get_student_by_id, name='get_student_by_id'),
    path('parent/<str:email>/', views.get_parent_by_email, name='get_parent_by_email'),
    path('parent-student-mapping/', views.create_parent_student_mapping, name='create_parent_student_mapping'),
    path('student-profiles/', views.get_student_profiles, name='get_student_profiles'),
    path('student-profile/<int:student_id>/', views.student_profile_detail, name='student_profile_detail'),
    path('create-student-profile/', views.create_student_profile, name='create_student_profile'),
    path('child-profile/', views.get_child_profile_for_parent, name='get_child_profile_for_parent'),
    path('parent-profile/', views.get_parent_profile_with_child_address, name='get_parent_profile_with_child_address'),
]
