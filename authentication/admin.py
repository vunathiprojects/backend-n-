from django.contrib import admin
from .models import (
    ParentRegistration,
    StudentRegistration,
    ParentStudentMapping,
    Class,
    User,
    Parent,
    Student,
    StudentProfile,
    PasswordResetToken
)

@admin.register(ParentRegistration)
class ParentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'email', 'first_name', 'last_name', 'phone_number', 'parent_username', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'parent_username')
    list_filter = ('created_at',)


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'student_username', 'student_email', 'parent_email', 'created_at')
    search_fields = ('first_name', 'last_name', 'student_username', 'student_email', 'parent_email')
    list_filter = ('created_at',)


@admin.register(ParentStudentMapping)
class ParentStudentMappingAdmin(admin.ModelAdmin):
    list_display = ('mapping_id', 'parent_email', 'student_id')
    search_fields = ('parent_email', 'student_id')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name')
    search_fields = ('class_name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'firstname', 'lastname', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'createdat')
    search_fields = ('username', 'firstname', 'lastname', 'email', 'role')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('userid',)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('parent',)
    search_fields = ('parent__username', 'parent__firstname', 'parent__lastname')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_field', 'parent')
    search_fields = ('student__username', 'student__firstname', 'student__lastname')
    list_filter = ('class_field',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'student_id', 'student_username', 'parent_email', 'grade', 'school', 'course_id')
    search_fields = ('student_username', 'parent_email', 'grade', 'school')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_used')
    search_fields = ('user__username', 'token')
    list_filter = ('is_used', 'created_at')
