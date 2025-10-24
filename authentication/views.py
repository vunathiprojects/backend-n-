from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
import uuid

from .models import (
    User, Student, Parent, PasswordResetToken,
    ParentRegistration, StudentRegistration, ParentStudentMapping, StudentProfile
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    PasswordChangeSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, StudentSerializer, ParentSerializer,
    ProfileUpdateSerializer, ParentRegistrationSerializer, StudentRegistrationSerializer,
    ParentStudentMappingSerializer, StudentProfileSerializer,
    ParentRegistrationCreateSerializer, StudentRegistrationCreateSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that includes user data in response
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Get user data
            username = request.data.get('username')
            user = User.objects.get(username=username)
            user_data = UserSerializer(user).data
            
            # Add user data to response
            response.data['user'] = user_data
            
            # Add role-specific data (optional - don't fail if profile doesn't exist)
            try:
                if user.role == 'Student' and hasattr(user, 'student'):
                    response.data['student_profile'] = StudentSerializer(user.student).data
                elif user.role == 'Parent' and hasattr(user, 'parent'):
                    response.data['parent_profile'] = ParentSerializer(user.parent).data
            except Exception as e:
                # Profile doesn't exist yet - that's okay for now
                pass
        
        return response


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Register a new user - Creates records in both User table and role-specific registration tables
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create role-specific records in registration tables (only tables that exist)
        if user.role == 'Student':
             # For students, we need to handle foreign key constraints
            parent_email = request.data.get('parent_email', '')
            
            # If parent_email is provided, check if parent exists
            if parent_email:
                try:
                    # Check if parent exists in parent_registration table
                    parent_exists = ParentRegistration.objects.filter(email=parent_email).exists()
                    if not parent_exists:
                        print(f"⚠️ Parent with email {parent_email} not found. Creating student without parent link.")
                        parent_email = ''  # Clear parent_email to avoid foreign key constraint
                except Exception as e:
                    print(f"⚠️ Error checking parent existence: {e}")
                    parent_email = ''
            
            # Create StudentRegistration record (for database compatibility)
            try:
                student_reg = StudentRegistration.objects.create(
                    student_username=user.username,
                    student_email=user.email,
                    first_name=user.firstname,
                    last_name=user.lastname,
                    phone_number=user.phonenumber,
                    parent_email=parent_email or 'no-parent@example.com'  # Use default if no parent
                )
                print(f"✅ Created StudentRegistration for {user.username} with student_id={student_reg.student_id}")
                
                # Create StudentProfile record (only with fields that exist in database)
                # Use student_reg.student_id (not user.userid) to satisfy foreign key constraint
                try:
                    StudentProfile.objects.create(
                        student_id=student_reg.student_id,  # Use StudentRegistration's student_id
                        student_username=user.username,
                        parent_email=parent_email or 'no-parent@example.com',
                        grade='',  # Empty for now
                        school='',  # Empty for now
                        course_id=None,  # Empty for now
                        address=''  # Empty for now
                    )
                    print(f"✅ Created StudentProfile for {user.username} with student_id={student_reg.student_id}")
                except Exception as e:
                    print(f"❌ Error creating StudentProfile: {e}")
                    
            except Exception as e:
                print(f"❌ Error creating StudentRegistration: {e}")
                
        elif user.role == 'Parent':
            # Create ParentRegistration record (for database compatibility)
            try:
                ParentRegistration.objects.create(
                    email=user.email,
                    first_name=user.firstname,
                    last_name=user.lastname,
                    phone_number=user.phonenumber,
                    parent_username=user.username,
                    parent_password=user.password  # Already hashed
                )
                print(f"✅ Created ParentRegistration for {user.username}")
            except Exception as e:
                print(f"❌ Error creating ParentRegistration: {e}")
                # Continue anyway - user is still created
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily disabled for testing
def get_user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    
    # Handle unauthenticated requests (for testing)
    if not user.is_authenticated:
        # Try to find srinu123 specifically for testing
        try:
            student_registration = StudentRegistration.objects.get(student_username='srinu123')
            # Create a mock user data structure
            response_data = {
                'userid': student_registration.student_id,
                'username': student_registration.student_username,
                'email': student_registration.student_email,
                'firstname': student_registration.first_name,
                'lastname': student_registration.last_name,
                'phonenumber': student_registration.phone_number,
                'role': 'Student',
                'createdat': student_registration.created_at
            }
            
            # Get student profile data
            try:
                student_profile = StudentProfile.objects.get(student_id=student_registration.student_id)
                response_data['student_profile'] = {
                    'student_username': student_profile.student_username,
                    'parent_email': student_profile.parent_email,
                    'grade': student_profile.grade,
                    'school': student_profile.school,
                    'address': student_profile.address
                }
            except StudentProfile.DoesNotExist:
                response_data['student_profile'] = {
                    'student_username': '',
                    'parent_email': '',
                    'grade': '',
                    'school': '',
                    'address': ''
                }
            
            return Response(response_data)
        except StudentRegistration.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to fetch profile: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Handle authenticated requests
    try:
        if user.role == 'Student':
            try:
                # Get student registration data
                student_registration = StudentRegistration.objects.get(student_username=user.username)
                response_data['student_registration'] = {
                    'first_name': student_registration.first_name,
                    'last_name': student_registration.last_name,
                    'phone_number': student_registration.phone_number,
                    'student_email': student_registration.student_email,
                    'student_username': student_registration.student_username,
                    'parent_email': student_registration.parent_email
                }
                
                # Get student profile data if exists
                try:
                    student_profile = StudentProfile.objects.get(student_id=student_registration.student_id)
                    response_data['student_profile'] = {
                        'student_username': student_profile.student_username,
                        'parent_email': student_profile.parent_email,
                        'grade': student_profile.grade,
                        'school': student_profile.school,
                        'address': student_profile.address
                    }
                except StudentProfile.DoesNotExist:
                    response_data['student_profile'] = {
                        'student_username': '',
                        'parent_email': '',
                        'grade': '',
                        'school': '',
                        'address': ''
                    }
                
                # Get parent details automatically if parent_email exists
                if student_registration.parent_email and student_registration.parent_email != 'no-parent@example.com':
                    try:
                        parent_registration = ParentRegistration.objects.get(email=student_registration.parent_email)
                        response_data['parent_details'] = {
                            'parent_name': f"{parent_registration.first_name} {parent_registration.last_name}",
                            'parent_email': parent_registration.email,
                            'parent_phone': parent_registration.phone_number
                        }
                    except ParentRegistration.DoesNotExist:
                        response_data['parent_details'] = {
                            'parent_name': 'Not provided',
                            'parent_email': 'Not provided',
                            'parent_phone': 'Not provided'
                        }
                else:
                    response_data['parent_details'] = {
                        'parent_name': 'Not provided',
                        'parent_email': 'Not provided',
                        'parent_phone': 'Not provided'
                    }
                    
            except StudentRegistration.DoesNotExist:
                response_data['student_registration'] = None
                response_data['student_profile'] = None
                response_data['parent_details'] = None
                
        elif user.role == 'Parent':
            try:
                # Get parent registration data
                parent_registration = ParentRegistration.objects.get(parent_username=user.username)
                response_data['parent_registration'] = {
                    'first_name': parent_registration.first_name,
                    'last_name': parent_registration.last_name,
                    'phone_number': parent_registration.phone_number,
                    'email': parent_registration.email,
                    'parent_username': parent_registration.parent_username
                }
            except ParentRegistration.DoesNotExist:
                response_data['parent_registration'] = None
        
        return Response(response_data)
    except Exception as e:
        return Response({'error': f'Failed to fetch profile: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_child_profile_for_parent(request):
    """
    Get child profile data for a parent user.
    Fetches student data from StudentRegistration and StudentProfile tables.
    """
    user = request.user
    
    if user.role != 'Parent':
        return Response({'error': 'Access denied. Only parent users can access this endpoint.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get parent registration data
        parent_registration = ParentRegistration.objects.get(parent_username=user.username)
        
        # Find student(s) linked to this parent via parent_email
        student_registrations = StudentRegistration.objects.filter(parent_email=parent_registration.email)
        
        if not student_registrations.exists():
            return Response({'error': 'No child found linked to this parent account.'}, 
                           status=status.HTTP_404_NOT_FOUND)
        
        # For now, get the first student (can be extended for multiple children)
        student_reg = student_registrations.first()
        
        # Get student profile data
        try:
            student_profile = StudentProfile.objects.get(student_id=student_reg.student_id)
        except StudentProfile.DoesNotExist:
            student_profile = None
        
        # Get user data for the student
        try:
            student_user = User.objects.get(username=student_reg.student_username)
        except User.DoesNotExist:
            student_user = None
        
        # Build response data
        response_data = {
            'student_registration': {
                'student_id': student_reg.student_id,
                'first_name': student_reg.first_name,
                'last_name': student_reg.last_name,
                'student_username': student_reg.student_username,
                'student_email': student_reg.student_email,
                'phone_number': student_reg.phone_number,
                'parent_email': student_reg.parent_email,
                'created_at': student_reg.created_at
            },
            'student_profile': {
                'profile_id': student_profile.profile_id if student_profile else None,
                'grade': student_profile.grade if student_profile else None,
                'school': student_profile.school if student_profile else None,
                'address': student_profile.address if student_profile else None,
                'course_id': student_profile.course_id if student_profile else None
            },
            'student_user': {
                'userid': student_user.userid if student_user else None,
                'username': student_user.username if student_user else None,
                'email': student_user.email if student_user else None,
                'phonenumber': student_user.phonenumber if student_user else None,
                'firstname': student_user.firstname if student_user else None,
                'lastname': student_user.lastname if student_user else None
            }
        }
        
        return Response(response_data)
        
    except ParentRegistration.DoesNotExist:
        return Response({'error': 'Parent registration not found.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Failed to fetch child profile: {str(e)}'}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_parent_profile_with_child_address(request):
    """
    Get parent profile data with child's address.
    Fetches parent contact info from ParentRegistration and child's address from StudentProfile.
    """
    user = request.user
    
    if user.role != 'Parent':
        return Response({'error': 'Access denied. Only parent users can access this endpoint.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get parent registration data
        parent_registration = ParentRegistration.objects.get(parent_username=user.username)
        
        # Find student(s) linked to this parent via parent_email
        student_registrations = StudentRegistration.objects.filter(parent_email=parent_registration.email)
        
        # Get child's address from student profile (use first child's address)
        child_address = 'Not specified'
        if student_registrations.exists():
            student_reg = student_registrations.first()
            try:
                student_profile = StudentProfile.objects.get(student_id=student_reg.student_id)
                child_address = student_profile.address if student_profile.address else 'Not specified'
            except StudentProfile.DoesNotExist:
                child_address = 'Not specified'
        
        # Build response data
        response_data = {
            'parent_registration': {
                'parent_id': parent_registration.parent_id,
                'first_name': parent_registration.first_name,
                'last_name': parent_registration.last_name,
                'email': parent_registration.email,
                'phone_number': parent_registration.phone_number,
                'parent_username': parent_registration.parent_username,
                'created_at': parent_registration.created_at
            },
            'child_address': child_address
        }
        
        return Response(response_data)
        
    except ParentRegistration.DoesNotExist:
        return Response({'error': 'Parent registration not found.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Failed to fetch parent profile: {str(e)}'}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    """
    Update current user profile
    """
    user = request.user
    serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': UserSerializer(user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Change user password
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_password_reset(request):
    """
    Request password reset
    """
    email = request.data.get('email')
    
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check if user exists in User model
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'No user found with this email address'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate reset token
    token = get_random_string(32)
    expires_at = datetime.now() + timedelta(hours=1)
    
    # Create or update reset token
    reset_token, created = PasswordResetToken.objects.get_or_create(
        user=user,
        defaults={'token': token, 'expires_at': expires_at}
    )
    
    if not created:
        reset_token.token = token
        reset_token.expires_at = expires_at
        reset_token.is_used = False
        reset_token.save()
    
    # For development, return the token (in production, send email)
    reset_url = f"http://localhost:3000/reset-password?token={token}"
    
    return Response({
        'message': 'Password reset link sent to your email',
        'reset_url': reset_url,  # Remove this in production
        'token': token  # Remove this in production
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def confirm_password_reset(request):
    """
    Confirm password reset
    """
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not token or not new_password or not confirm_password:
        return Response({'error': 'Token, new password, and confirm password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if new_password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 6:
        return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False,
            expires_at__gt=datetime.now()
        )
        
        # Update user password
        user = reset_token.user
        user.set_password(new_password)
        user.save()
        
        # Also update password in the new schema if it exists
        if user.role == 'Parent':
            try:
                parent = ParentRegistration.objects.get(email=user.email)
                from django.contrib.auth.hashers import make_password
                parent.parent_password = make_password(new_password)
                parent.save()
            except ParentRegistration.DoesNotExist:
                pass
        
        # Mark token as used
        reset_token.is_used = True
        reset_token.save()
        
        return Response({'message': 'Password reset successfully'})
    
    except PasswordResetToken.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired reset token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """
    Logout user (blacklist refresh token)
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentListCreateView(generics.ListCreateAPIView):
    """
    List and create students
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Parents can only see their children
        if self.request.user.role == 'parent':
            return Student.objects.filter(parent__parent=self.request.user)
        return Student.objects.all()


class ParentListCreateView(generics.ListCreateAPIView):
    """
    List and create parents
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_dashboard_data(request):
    """
    Get dashboard data based on user role
    """
    user = request.user
    
    if user.role == 'student':
        # Student dashboard data
        from courses.models import CourseEnrollment
        from progress.models import StudentProgress, Assignment
        from quizzes.models import QuizAttempt
        
        enrollments = CourseEnrollment.objects.filter(student=user, is_active=True)
        progress_records = StudentProgress.objects.filter(student=user)
        assignments = Assignment.objects.filter(assigned_to=user)
        quiz_attempts = QuizAttempt.objects.filter(student=user)
        
        dashboard_data = {
            'user': UserSerializer(user).data,
            'enrolled_courses': enrollments.count(),
            'overall_progress': sum([p.overall_percentage for p in progress_records]) / len(progress_records) if progress_records else 0,
            'pending_assignments': assignments.filter(due_date__gt=datetime.now()).count(),
            'completed_assignments': assignments.filter(submissions__student=user).count(),
            'quizzes_taken': quiz_attempts.count(),
            'average_quiz_score': sum([a.score for a in quiz_attempts]) / len(quiz_attempts) if quiz_attempts else 0,
        }
        
    elif user.role == 'parent':
        # Parent dashboard data
        from progress.models import StudentProgress
        
        children = Student.objects.filter(parent__parent=user)
        children_progress = []
        
        for child in children:
            progress_records = StudentProgress.objects.filter(student=child.student)
            children_progress.append({
                'child': UserSerializer(child.student).data,
                'overall_progress': sum([p.overall_percentage for p in progress_records]) / len(progress_records) if progress_records else 0,
                'subjects_count': progress_records.count(),
            })
        
        dashboard_data = {
            'user': UserSerializer(user).data,
            'children': [UserSerializer(child.student).data for child in children],
            'children_progress': children_progress,
        }
        
    
    else:
        dashboard_data = {
            'user': UserSerializer(user).data,
        }
    
    return Response(dashboard_data)


# New views for the updated schema

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_parent(request):
    """
    Register a new parent
    """
    serializer = ParentRegistrationCreateSerializer(data=request.data)
    if serializer.is_valid():
        parent = serializer.save()
        
        # Also create a User entry for authentication
        try:
            user = User.objects.create_user(
                username=parent.parent_username,
                email=parent.email,
                firstname=parent.first_name,
                lastname=parent.last_name,
                phonenumber=parent.phone_number,
                role='Parent',
                password=request.data.get('parent_password')  # This will be hashed by create_user
            )
            
            # Create Parent profile
            Parent.objects.create(parent=user)
            
        except Exception as e:
            # If User creation fails, delete the parent registration
            parent.delete()
            return Response({
                'error': f'Failed to create user account: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Parent registered successfully',
            'parent': ParentRegistrationSerializer(parent).data,
            'user_id': user.userid
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_student(request):
    """
    Register a new student
    """
    serializer = StudentRegistrationCreateSerializer(data=request.data)
    if serializer.is_valid():
        student = serializer.save()
        
        # Get password from the serializer's validated data
        password = request.data.get('password')
        
        # Also create a User entry for authentication
        try:
            # Ensure we have a valid email for the user
            user_email = student.student_email
            if not user_email:
                user_email = f"{student.student_username}@student.novya.com"
            
            # Check if phone number is already in use
            phone_number = student.phone_number
            if User.objects.filter(phonenumber=phone_number).exists():
                # Generate a unique phone number by appending a suffix
                counter = 1
                while User.objects.filter(phonenumber=f"{phone_number}_{counter}").exists():
                    counter += 1
                phone_number = f"{phone_number}_{counter}"
                print(f"Warning: Phone number conflict resolved by using: {phone_number}")
            
            user = User.objects.create_user(
                username=student.student_username,
                email=user_email,
                firstname=student.first_name,
                lastname=student.last_name,
                phonenumber=phone_number,
                role='Student',
                password=password  # Add password here
            )
            
            # Create Student profile
            # Try to find the parent if it exists
            parent_obj = None
            try:
                parent_registration = ParentRegistration.objects.get(email=student.parent_email)
                # Find the corresponding User and Parent objects
                parent_user = User.objects.get(email=student.parent_email)
                parent_obj = Parent.objects.get(parent=parent_user)
            except (ParentRegistration.DoesNotExist, User.DoesNotExist, Parent.DoesNotExist):
                # Parent doesn't exist yet, create student without parent link
                pass
            
            # Create Student model with error handling
            try:
                Student.objects.create(student=user, parent=parent_obj)
            except Exception as student_error:
                # If Student creation fails, log the error but don't fail the registration
                print(f"Warning: Could not create Student model: {student_error}")
                # Continue with registration even if Student model creation fails
            
        except Exception as e:
            # If User creation fails, delete the student registration
            student.delete()
            return Response({
                'error': f'Failed to create user account: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Student registered successfully',
            'student': StudentRegistrationSerializer(student).data,
            'user_id': user.userid
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Changed to AllowAny for testing
def get_parents(request):
    """
    Get all parents
    """
    parents = ParentRegistration.objects.all()
    serializer = ParentRegistrationSerializer(parents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Changed to AllowAny for testing
def get_students(request):
    """
    Get all students
    """
    students = StudentRegistration.objects.all()
    serializer = StudentRegistrationSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_by_id(request, student_id):
    """
    Get student by ID
    """
    try:
        student = StudentRegistration.objects.get(student_id=student_id)
        serializer = StudentRegistrationSerializer(student)
        return Response(serializer.data)
    except StudentRegistration.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_parent_by_email(request, email):
    """
    Get parent by email
    """
    try:
        parent = ParentRegistration.objects.get(email=email)
        serializer = ParentRegistrationSerializer(parent)
        return Response(serializer.data)
    except ParentRegistration.DoesNotExist:
        return Response(
            {'error': 'Parent not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_parent_student_mapping(request):
    """
    Create parent-student mapping
    """
    serializer = ParentStudentMappingSerializer(data=request.data)
    if serializer.is_valid():
        mapping = serializer.save()
        return Response({
            'message': 'Parent-student mapping created successfully',
            'mapping': ParentStudentMappingSerializer(mapping).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_profiles(request):
    """
    Get all student profiles
    """
    profiles = StudentProfile.objects.all()
    serializer = StudentProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def student_profile_detail(request, student_id):
    """
    Get or update student profile
    """
    try:
        profile = StudentProfile.objects.get(student_id=student_id)
    except StudentProfile.DoesNotExist:
        return Response(
            {'error': 'Student profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = StudentProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Student profile updated successfully',
                'profile': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_student_profile(request):
    """
    Create student profile
    """
    serializer = StudentProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save()
        return Response({
            'message': 'Student profile created successfully',
            'profile': StudentProfileSerializer(profile).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily disabled for testing
def get_user_profile_data(request):
    """
    Get user profile data including student registration and profile
    """
    user = request.user
    
    # Handle unauthenticated requests (for testing)
    if not user.is_authenticated:
        # Try to find srinu123 specifically for testing
        try:
            student_registration = StudentRegistration.objects.get(student_username='srinu123')
        except StudentRegistration.DoesNotExist:
            # Fallback to first student if srinu123 not found
            try:
                student_registration = StudentRegistration.objects.first()
                if not student_registration:
                    return Response({'error': 'No student data found'}, status=status.HTTP_404_NOT_FOUND)
            except StudentRegistration.DoesNotExist:
                return Response({'error': 'No student registration found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            # Get student registration data
            student_registration = StudentRegistration.objects.get(student_username=user.username)
        except StudentRegistration.DoesNotExist:
            return Response({'error': 'Student registration not found for this user'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        
        # Get student profile data
        try:
            student_profile = StudentProfile.objects.get(student_id=student_registration.student_id)
            profile_data = {
                'student_username': student_profile.student_username,
                'parent_email': student_profile.parent_email,
                'grade': student_profile.grade,
                'school': student_profile.school,
                'address': student_profile.address
            }
        except StudentProfile.DoesNotExist:
            profile_data = {
                'student_username': '',
                'parent_email': '',
                'grade': '',
                'school': '',
                'address': ''
            }
        
        # Get parent details automatically if parent_email exists
        parent_details = {}
        if student_registration.parent_email and student_registration.parent_email != 'no-parent@example.com':
            try:
                parent_registration = ParentRegistration.objects.get(email=student_registration.parent_email)
                parent_details = {
                    'parent_name': f"{parent_registration.first_name} {parent_registration.last_name}",
                    'parent_email': parent_registration.email,
                    'parent_phone': parent_registration.phone_number
                }
            except ParentRegistration.DoesNotExist:
                parent_details = {
                    'parent_name': 'Not provided',
                    'parent_email': 'Not provided',
                    'parent_phone': 'Not provided'
                }
        else:
            parent_details = {
                'parent_name': 'Not provided',
                'parent_email': 'Not provided',
                'parent_phone': 'Not provided'
            }
        
        # Prepare user data
        if user.is_authenticated:
            user_data = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'username': user.username
            }
        else:
            # Use student registration data for unauthenticated requests
            user_data = {
                'firstname': student_registration.first_name,
                'lastname': student_registration.last_name,
                'email': student_registration.student_email,
                'phonenumber': student_registration.phone_number,
                'username': student_registration.student_username
            }
        
        return Response({
            'user': user_data,
            'student_registration': {
                'first_name': student_registration.first_name,
                'last_name': student_registration.last_name,
                'phone_number': student_registration.phone_number,
                'student_email': student_registration.student_email,
                'student_username': student_registration.student_username,
                'parent_email': student_registration.parent_email
            },
            'student_profile': profile_data,
            'parent_details': parent_details
        }, status=status.HTTP_200_OK)
        
    except StudentRegistration.DoesNotExist:
        return Response({
            'error': 'Student registration not found for this user'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Failed to get profile data: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.AllowAny])  # Temporarily disabled for testing
def update_user_profile(request):
    """
    Update user profile and student profile together
    """
    user = request.user
    
    try:
        # Handle unauthenticated requests (for testing)
        if not user.is_authenticated:
            # Try to find the student by username from the request data
            requested_username = request.data.get('userName')
            if requested_username:
                try:
                    student_registration = StudentRegistration.objects.get(student_username=requested_username)
                except StudentRegistration.DoesNotExist:
                    # Fallback to first student if username not found
                    student_registration = StudentRegistration.objects.first()
            else:
                # Use the first student for testing
                student_registration = StudentRegistration.objects.first()
            
            if not student_registration:
                return Response({'error': 'No student data found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                # Update User model fields
                user.firstname = request.data.get('firstName', user.firstname)
                user.lastname = request.data.get('lastName', user.lastname)
                user.email = request.data.get('email', user.email)
                user.phonenumber = request.data.get('phone', user.phonenumber)
                user.save()
                
                # Update StudentRegistration fields
                student_registration = StudentRegistration.objects.get(student_username=user.username)
            except StudentRegistration.DoesNotExist:
                return Response({'error': 'Student registration not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update StudentRegistration fields
        student_registration.first_name = request.data.get('firstName', student_registration.first_name)
        student_registration.last_name = request.data.get('lastName', student_registration.last_name)
        
        # Only update phone number if it's different to avoid unique constraint violation
        new_phone = request.data.get('phone', student_registration.phone_number)
        if new_phone != student_registration.phone_number:
            # Check if the new phone number is already in use by another student
            if StudentRegistration.objects.filter(phone_number=new_phone).exclude(student_id=student_registration.student_id).exists():
                print(f"Warning: Phone number {new_phone} is already in use by another student")
            else:
                student_registration.phone_number = new_phone
        
        # Only update email if it's different to avoid unique constraint violation
        new_email = request.data.get('email', student_registration.student_email)
        if new_email != student_registration.student_email:
            # Check if the new email is already in use by another student
            if StudentRegistration.objects.filter(student_email=new_email).exclude(student_id=student_registration.student_id).exists():
                print(f"Warning: Email {new_email} is already in use by another student")
            else:
                student_registration.student_email = new_email
        
        # Only update username if it's different to avoid unique constraint violation
        new_username = request.data.get('userName', student_registration.student_username)
        if new_username != student_registration.student_username:
            # Check if the new username is already in use by another student
            if StudentRegistration.objects.filter(student_username=new_username).exclude(student_id=student_registration.student_id).exists():
                print(f"Warning: Username {new_username} is already in use by another student")
            else:
                student_registration.student_username = new_username
        
        # Only update parent_email if it exists in parent_registration table
        new_parent_email = request.data.get('parentEmail', student_registration.parent_email)
        if new_parent_email and new_parent_email != student_registration.parent_email:
            # Check if parent exists (ParentRegistration uses 'email' field, not 'parent_email')
            try:
                ParentRegistration.objects.get(email=new_parent_email)
                student_registration.parent_email = new_parent_email
            except ParentRegistration.DoesNotExist:
                # Keep existing parent_email if new one doesn't exist
                print(f"Warning: Parent email {new_parent_email} not found in parent_registration table")
        
        student_registration.save()
        
        # Get or create StudentProfile
        student_profile, created = StudentProfile.objects.get_or_create(
            student_id=student_registration.student_id,
            defaults={
                'student_username': request.data.get('userName', ''),
                'parent_email': student_registration.parent_email,  # Use the validated parent_email
                'grade': request.data.get('grade', ''),
                'school': request.data.get('school', ''),
                'address': request.data.get('address', ''),
            }
        )
        
        if not created:
            # Update existing profile
            # Only update username if it's different to avoid unique constraint violation
            new_profile_username = request.data.get('userName', student_profile.student_username)
            if new_profile_username != student_profile.student_username:
                # Check if the new username is already in use by another profile
                if StudentProfile.objects.filter(student_username=new_profile_username).exclude(profile_id=student_profile.profile_id).exists():
                    print(f"Warning: Username {new_profile_username} is already in use by another profile")
                else:
                    student_profile.student_username = new_profile_username
            
            student_profile.parent_email = student_registration.parent_email  # Use the validated parent_email
            student_profile.grade = request.data.get('grade', student_profile.grade)
            student_profile.school = request.data.get('school', student_profile.school)
            student_profile.address = request.data.get('address', student_profile.address)
            student_profile.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'firstname': student_registration.first_name,
                'lastname': student_registration.last_name,
                'email': student_registration.student_email,
                'phonenumber': student_registration.phone_number,
                'username': student_registration.student_username
            },
            'student_registration': {
                'first_name': student_registration.first_name,
                'last_name': student_registration.last_name,
                'phone_number': student_registration.phone_number,
                'student_email': student_registration.student_email,
                'student_username': student_registration.student_username,
                'parent_email': student_registration.parent_email
            },
            'student_profile': {
                'student_username': student_profile.student_username,
                'parent_email': student_profile.parent_email,
                'grade': student_profile.grade,
                'school': student_profile.school,
                'address': student_profile.address
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to update profile: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
