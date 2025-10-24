# NOVYA LMS Backend

A comprehensive Django REST API backend for the NOVYA Learning Management System.

## Features

- **User Authentication**: JWT-based authentication for Students, Parents, and Teachers
- **Course Management**: Subjects, Courses, Chapters, and Lessons
- **Quiz System**: Practice tests with multiple choice questions and analytics
- **Progress Tracking**: Student progress, attendance, and achievements
- **Parent Dashboard**: Monitor child's academic progress
- **Notifications**: Events, announcements, and messaging system
- **Study Planning**: Personalized study plans and schedules

## Setup Instructions

### 1. Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings (PostgreSQL)
DB_NAME=novya_lms
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Email Settings (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Celery Settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Media and Static Files
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/django.log
```

### 2. Install Dependencies

```bash
pip install -r requirements.py
```

### 3. Database Setup (Local PostgreSQL)

#### Option A: Automated Setup (Recommended)
```bash
# Windows
setup_windows.bat

# macOS
./setup_macos.sh

# Linux
./setup_linux.sh
```

#### Option B: Manual Setup
1. **Install PostgreSQL locally:**
   - **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - **macOS**: `brew install postgresql@15`
   - **Linux**: `sudo apt install postgresql postgresql-contrib`

2. **Start PostgreSQL service:**
   - **Windows**: `net start postgresql`
   - **macOS**: `brew services start postgresql@15`
   - **Linux**: `sudo systemctl start postgresql`

3. **Create database:**
   ```sql
   psql -U postgres
   CREATE DATABASE novya_lms;
   \q
   ```

4. **Update .env file with your PostgreSQL password**

5. **Run Django setup:**
   ```bash
   python setup_local_postgresql.py
   ```

#### Test Database Connection
```bash
python test_db_connection.py
```

#### Detailed Setup Guide
For comprehensive instructions, see [LOCAL_POSTGRESQL_SETUP.md](LOCAL_POSTGRESQL_SETUP.md)

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Populate Initial Data

```bash
python manage.py populate_initial_data
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password
- `POST /api/auth/request-password-reset/` - Request password reset
- `POST /api/auth/confirm-password-reset/` - Confirm password reset

### Courses
- `GET /api/courses/subjects/` - List subjects
- `GET /api/courses/` - List courses
- `GET /api/courses/{id}/` - Course details
- `GET /api/courses/{id}/chapters/` - Course chapters
- `GET /api/courses/{id}/chapters/{id}/lessons/` - Chapter lessons
- `POST /api/courses/{id}/enroll/` - Enroll in course
- `GET /api/courses/{id}/progress/` - Course progress
- `POST /api/courses/lessons/{id}/progress/` - Update lesson progress

### Quizzes
- `GET /api/quizzes/` - List available quizzes
- `GET /api/quizzes/{id}/` - Quiz details
- `POST /api/quizzes/{id}/start/` - Start quiz
- `POST /api/quizzes/{id}/submit/` - Submit quiz
- `GET /api/quizzes/attempts/` - My quiz attempts
- `GET /api/quizzes/attempts/{id}/` - Quiz attempt details
- `GET /api/quizzes/stats/` - Quiz statistics

### Progress & Attendance
- `GET /api/progress/dashboard/` - Student dashboard
- `GET /api/progress/attendance/` - Attendance records
- `GET /api/progress/assignments/` - My assignments
- `POST /api/progress/assignments/{id}/submit/` - Submit assignment
- `GET /api/progress/grades/` - My grades
- `GET /api/progress/achievements/` - My achievements

### Parent Dashboard
- `GET /api/progress/parent-dashboard/` - Parent dashboard data
- `GET /api/progress/children/` - Children list

### Notifications
- `GET /api/notifications/` - My notifications
- `POST /api/notifications/{id}/read/` - Mark notification as read
- `GET /api/notifications/events/` - Available events
- `POST /api/notifications/events/{id}/register/` - Register for event
- `GET /api/notifications/announcements/` - Announcements
- `GET /api/notifications/messages/` - Messages
- `POST /api/notifications/messages/` - Send message

## User Roles

### Student
- Access to enrolled courses
- Take quizzes and practice tests
- Submit assignments
- View progress and achievements
- Access study materials

### Parent
- Monitor child's progress
- View attendance records
- Access child's grades and assignments
- Receive notifications about child's activities

### Teacher
- Create and manage courses
- Assign homework and quizzes
- Grade assignments
- Track student progress
- Send announcements

## Database Models

### Core Models
- **User**: Custom user model with role-based authentication
- **Student**: Student profile with grade and parent information
- **Parent**: Parent profile with occupation details
- **Teacher**: Teacher profile with qualifications and experience

### Course Models
- **Subject**: Academic subjects (Math, Science, English, etc.)
- **Course**: Course instances for specific grades
- **Chapter**: Course chapters with lessons
- **Lesson**: Individual lessons with content and materials
- **CourseEnrollment**: Student course enrollments

### Quiz Models
- **Quiz**: Practice tests and assessments
- **Question**: Quiz questions with multiple types
- **QuestionOption**: Answer options for multiple choice questions
- **QuizAttempt**: Student quiz attempts
- **QuizAnswer**: Individual question answers
- **QuizResult**: Detailed quiz results and analytics

### Progress Models
- **StudentProgress**: Overall student progress tracking
- **Attendance**: Class attendance records
- **Assignment**: Homework and assignments
- **AssignmentSubmission**: Student assignment submissions
- **Grade**: Assignment and quiz grades
- **Achievement**: Student achievements and badges

### Notification Models
- **Event**: School events and activities
- **EventRegistration**: Event registrations
- **Notification**: System notifications
- **Announcement**: School announcements
- **Message**: Internal messaging system
- **Feedback**: User feedback and support

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .

# Check code style
flake8 .

# Sort imports
isort .
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Production Deployment

1. Set `DEBUG=False` in environment variables
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for Celery
4. Configure email backend
5. Set up static file serving
6. Configure CORS for production domain
7. Set up SSL certificates
8. Configure logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.
