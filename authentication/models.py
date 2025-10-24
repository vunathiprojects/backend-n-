from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class ParentRegistration(models.Model):
    """
    Parent Registration model matching new schema
    """
    parent_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)  # Primary key in DB but not Django
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?[\d\s\-\(\)]{9,15}$', message="Phone number must be entered in a valid format. Up to 15 digits allowed.")]
    )
    parent_username = models.CharField(max_length=255, unique=True)
    parent_password = models.CharField(max_length=255)  # This will be hashed
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.parent_username})"
    
    class Meta:
        db_table = 'parent_registration'
        verbose_name = 'Parent Registration'
        verbose_name_plural = 'Parent Registrations'


class StudentRegistration(models.Model):
    """
    Student Registration model matching new schema
    """
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?[\d\s\-\(\)]{9,15}$', message="Phone number must be entered in a valid format. Up to 15 digits allowed.")]
    )
    student_username = models.CharField(max_length=255, unique=True)
    student_email = models.EmailField(unique=True, null=True, blank=True)
    parent_email = models.EmailField()  # Changed from ForeignKey to EmailField
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_username})"
    
    class Meta:
        db_table = 'student_registration'
        verbose_name = 'Student Registration'
        verbose_name_plural = 'Student Registrations'


class ParentStudentMapping(models.Model):
    """
    Parent-Student Mapping model matching new schema
    """
    mapping_id = models.AutoField(primary_key=True)
    parent_email = models.EmailField()  # Changed from ForeignKey to EmailField
    student_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    
    def __str__(self):
        return f"Parent: {self.parent_email} -> Student: {self.student_id}"
    
    class Meta:
        db_table = 'parent_student_mapping'
        verbose_name = 'Parent Student Mapping'
        verbose_name_plural = 'Parent Student Mappings'


class Class(models.Model):
    """
    Class model matching new schema
    """
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.class_name
    
    class Meta:
        db_table = 'class'
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'


class UserManager(BaseUserManager):
    """
    Custom user manager for our User model
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


# Legacy User model for backward compatibility
class User(AbstractBaseUser, PermissionsMixin):
    """
    Legacy User model for backward compatibility
    """
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Parent', 'Parent'),
        ('Admin', 'Admin'),
    ]

    userid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    phonenumber = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?[\d\s\-\(\)]{9,15}$', message="Phone number must be entered in a valid format. Up to 15 digits allowed.")]
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Student')
    createdat = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Required fields for Django auth compatibility
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname']
    
    objects = UserManager()
    
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}".strip()
    
    def get_short_name(self):
        return self.firstname
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.username})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# Legacy models for backward compatibility
class Parent(models.Model):
    """
    Legacy Parent model for backward compatibility
    """
    parent = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"{self.parent.firstname} {self.parent.lastname} (Parent)"
    
    class Meta:
        db_table = 'parent'
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'


class Student(models.Model):
    """
    Legacy Student model for backward compatibility
    """
    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, db_column='class_id')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname} - {self.class_field.class_name if self.class_field else 'No Class'}"
    
    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'




class StudentProfile(models.Model):
    """
    Student Profile model matching actual database schema
    """
    profile_id = models.AutoField(primary_key=True)
    student_id = models.IntegerField(unique=True)  # Changed from OneToOneField to IntegerField
    student_username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    parent_email = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=150, null=True, blank=True)
    course_id = models.IntegerField(null=True, blank=True)  # Changed from ForeignKey to IntegerField
    address = models.TextField(null=True, blank=True)
    # Only include fields that actually exist in the database
    
    def __str__(self):
        return f"Profile for Student ID: {self.student_id}"
    
    class Meta:
        db_table = 'student_profile'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'


class PasswordResetToken(models.Model):
    """
    Password reset token model
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    class Meta:
        db_table = 'authentication_password_reset_token'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'