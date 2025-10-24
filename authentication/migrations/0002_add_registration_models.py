# Generated manually to add missing registration models

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentRegistration',
            fields=[
                ('parent_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in a valid format. Up to 15 digits allowed.", regex='^\\+?[\\d\\s\\-\\(\\)]{9,15}$')])),
                ('parent_username', models.CharField(max_length=255, unique=True)),
                ('parent_password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Parent Registration',
                'verbose_name_plural': 'Parent Registrations',
                'db_table': 'parent_registration',
            },
        ),
        migrations.CreateModel(
            name='StudentRegistration',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in a valid format. Up to 15 digits allowed.", regex='^\\+?[\\d\\s\\-\\(\\)]{9,15}$')])),
                ('student_username', models.CharField(max_length=255, unique=True)),
                ('student_email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('parent_email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Student Registration',
                'verbose_name_plural': 'Student Registrations',
                'db_table': 'student_registration',
            },
        ),
        migrations.CreateModel(
            name='ParentStudentMapping',
            fields=[
                ('mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_email', models.EmailField(max_length=254)),
                ('student_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Parent Student Mapping',
                'verbose_name_plural': 'Parent Student Mappings',
                'db_table': 'parent_student_mapping',
            },
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField(unique=True)),
                ('student_username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('parent_email', models.CharField(blank=True, max_length=255, null=True)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('school', models.CharField(blank=True, max_length=150, null=True)),
                ('course_id', models.IntegerField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Student Profile',
                'verbose_name_plural': 'Student Profiles',
                'db_table': 'student_profile',
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
            options={
                'verbose_name': 'Password Reset Token',
                'verbose_name_plural': 'Password Reset Tokens',
                'db_table': 'authentication_password_reset_token',
            },
        ),
    ]
