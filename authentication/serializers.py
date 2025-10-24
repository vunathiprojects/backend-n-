from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import (
    User, Student, Parent, PasswordResetToken, 
    ParentRegistration, StudentRegistration, ParentStudentMapping, StudentProfile
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'userid', 'username', 'email', 'firstname', 'lastname', 'full_name',
            'role', 'phonenumber', 'createdat'
        ]
        read_only_fields = ['userid', 'createdat']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'firstname', 'lastname', 'password',
            'confirm_password', 'role', 'phonenumber'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email address')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation
    """
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model
    """
    student_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'student', 'class_field', 'parent', 'student_name', 'class_name'
        ]
        read_only_fields = ['student']
    
    def get_student_name(self, obj):
        return f"{obj.student.firstname} {obj.student.lastname}"
    
    def get_class_name(self, obj):
        return obj.class_field.class_name if obj.class_field else None


class ParentSerializer(serializers.ModelSerializer):
    """
    Serializer for Parent model
    """
    parent_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Parent
        fields = [
            'parent', 'parent_name'
        ]
        read_only_fields = ['parent']
    
    def get_parent_name(self, obj):
        return f"{obj.parent.firstname} {obj.parent.lastname}"




class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for profile updates
    """
    class Meta:
        model = User
        fields = [
            'firstname', 'lastname', 'email', 'phonenumber'
        ]
    
    def update(self, instance, validated_data):
        # Handle profile picture upload
        if 'profile_picture' in validated_data:
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
        return super().update(instance, validated_data)


# New serializers for the updated schema

class ParentRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for Parent Registration
    """
    class Meta:
        model = ParentRegistration
        fields = [
            'parent_id', 'email', 'first_name', 'last_name', 
            'phone_number', 'parent_username', 'parent_password', 'created_at'
        ]
        read_only_fields = ['parent_id', 'created_at']
        extra_kwargs = {
            'parent_password': {'write_only': True}
        }


class StudentRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for Student Registration
    """
    class Meta:
        model = StudentRegistration
        fields = [
            'student_id', 'first_name', 'last_name', 'phone_number',
            'student_username', 'student_email', 'parent_email', 'created_at'
        ]
        read_only_fields = ['student_id', 'created_at']


class ParentStudentMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for Parent-Student Mapping
    """
    parent_email = serializers.EmailField()
    student_id = serializers.IntegerField()
    
    class Meta:
        model = ParentStudentMapping
        fields = ['mapping_id', 'parent_email', 'student_id']
        read_only_fields = ['mapping_id']


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Student Profile
    """
    student_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = [
            'profile_id', 'student_id', 'student_username', 'parent_email',
            'grade', 'school', 'course_id', 'address', 'updated_at', 'student_name',
            'gender', 'date_of_birth', 'subjects', 'class_teacher', 'progress', 'parent_name'
        ]
        read_only_fields = ['profile_id', 'updated_at']
    
    def get_student_name(self, obj):
        try:
            student = StudentRegistration.objects.get(student_id=obj.student_id)
            return f"{student.first_name} {student.last_name}"
        except StudentRegistration.DoesNotExist:
            return "Unknown Student"


class ParentRegistrationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating parent registration
    """
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = ParentRegistration
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'parent_username', 'parent_password', 'confirm_password'
        ]
        extra_kwargs = {
            'parent_password': {'write_only': True}
        }
    
    def validate(self, attrs):
        if attrs['parent_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        # Hash the password
        from django.contrib.auth.hashers import make_password
        validated_data['parent_password'] = make_password(validated_data['parent_password'])
        return ParentRegistration.objects.create(**validated_data)


class StudentRegistrationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating student registration
    """
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = StudentRegistration
        fields = [
            'first_name', 'last_name', 'phone_number',
            'student_username', 'student_email', 'parent_email',
            'password', 'confirm_password'
        ]
    
    def to_internal_value(self, data):
        """Override to handle phone number conflicts before validation"""
        # Handle phone number conflicts
        if 'phone_number' in data:
            phone_number = data['phone_number']
            if StudentRegistration.objects.filter(phone_number=phone_number).exists():
                # Generate a unique phone number by modifying the last digit
                base_phone = phone_number[:-1]  # Remove last digit
                last_digit = int(phone_number[-1])
                counter = 1
                while StudentRegistration.objects.filter(phone_number=f"{base_phone}{(last_digit + counter) % 10}").exists():
                    counter += 1
                data['phone_number'] = f"{base_phone}{(last_digit + counter) % 10}"
                print(f"Warning: Phone number conflict resolved by using: {data['phone_number']}")
        
        return super().to_internal_value(data)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Check if parent exists
        try:
            ParentRegistration.objects.get(email=validated_data['parent_email'])
        except ParentRegistration.DoesNotExist:
            raise serializers.ValidationError("Parent with this email does not exist")
        
        # Remove password fields from validated_data before creating StudentRegistration
        validated_data.pop('password')
        validated_data.pop('confirm_password')
        
        return StudentRegistration.objects.create(**validated_data)
