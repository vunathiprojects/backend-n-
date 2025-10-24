from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Subject, Course, Chapter, Lesson
from authentication.models import Student, Parent, Teacher

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate initial data for the LMS system'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate initial data...')

        # Create subjects
        subjects_data = [
            {'name': 'Mathematics', 'description': 'Mathematical concepts and problem solving', 'icon': '📊', 'color': '#FF6B6B'},
            {'name': 'Science', 'description': 'Physics, Chemistry, and Biology', 'icon': '⚗️', 'color': '#4ECDC4'},
            {'name': 'English', 'description': 'Language and Literature', 'icon': '📚', 'color': '#45B7D1'},
            {'name': 'Social Studies', 'description': 'History, Geography, and Civics', 'icon': '🏛️', 'color': '#96CEB4'},
            {'name': 'Computer Science', 'description': 'Computer basics and programming', 'icon': '💻', 'color': '#FFEAA7'},
        ]

        subjects = {}
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults=subject_data
            )
            subjects[subject_data['name']] = subject
            if created:
                self.stdout.write(f'Created subject: {subject.name}')

        # Create sample users
        # Create a teacher
        teacher_user, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'email': 'teacher@novya.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'teacher',
                'is_active': True
            }
        )
        if created:
            teacher_user.set_password('teacher123')
            teacher_user.save()
            Teacher.objects.create(
                user=teacher_user,
                employee_id='T001',
                department='Mathematics',
                qualification='M.Sc Mathematics',
                experience_years=5
            )
            self.stdout.write('Created teacher: John Smith')

        # Create a parent
        parent_user, created = User.objects.get_or_create(
            username='parent1',
            defaults={
                'email': 'parent@novya.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'role': 'parent',
                'is_active': True
            }
        )
        if created:
            parent_user.set_password('parent123')
            parent_user.save()
            parent_profile = Parent.objects.create(
                user=parent_user,
                occupation='Engineer',
                workplace='Tech Corp'
            )
            self.stdout.write('Created parent: Jane Doe')

        # Create a student
        student_user, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student@novya.com',
                'first_name': 'Alex',
                'last_name': 'Johnson',
                'role': 'student',
                'is_active': True
            }
        )
        if created:
            student_user.set_password('student123')
            student_user.save()
            Student.objects.create(
                user=student_user,
                grade='7',
                roll_number='S001',
                parent=parent_profile
            )
            self.stdout.write('Created student: Alex Johnson')

        # Create sample courses
        courses_data = [
            {
                'title': 'Mathematics Grade 7',
                'description': 'Comprehensive mathematics course for grade 7 students',
                'subject': 'Mathematics',
                'grade': '7',
                'duration_hours': 40
            },
            {
                'title': 'Science Grade 7',
                'description': 'Introduction to physics, chemistry, and biology',
                'subject': 'Science',
                'grade': '7',
                'duration_hours': 35
            },
            {
                'title': 'English Grade 7',
                'description': 'Language skills and literature',
                'subject': 'English',
                'grade': '7',
                'duration_hours': 30
            },
            {
                'title': 'Social Studies Grade 7',
                'description': 'History, geography, and civics',
                'subject': 'Social Studies',
                'grade': '7',
                'duration_hours': 25
            },
            {
                'title': 'Computer Science Grade 7',
                'description': 'Computer basics and digital literacy',
                'subject': 'Computer Science',
                'grade': '7',
                'duration_hours': 20
            }
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'subject': subjects[course_data['subject']],
                    'grade': course_data['grade'],
                    'instructor': teacher_user,
                    'duration_hours': course_data['duration_hours'],
                    'is_published': True
                }
            )
            if created:
                self.stdout.write(f'Created course: {course.title}')

                # Create chapters for each course
                if course_data['subject'] == 'Mathematics':
                    chapters_data = [
                        {'title': 'Large Numbers', 'chapter_number': 1},
                        {'title': 'Arithmetic Expressions', 'chapter_number': 2},
                        {'title': 'Peek Point', 'chapter_number': 3},
                        {'title': 'Number Expressions', 'chapter_number': 4},
                        {'title': 'Lines', 'chapter_number': 5},
                    ]
                elif course_data['subject'] == 'Science':
                    chapters_data = [
                        {'title': 'Age of Science', 'chapter_number': 1},
                        {'title': 'Substances', 'chapter_number': 2},
                        {'title': 'Electricity', 'chapter_number': 3},
                        {'title': 'Metals', 'chapter_number': 4},
                        {'title': 'Physical and Chemical Changes', 'chapter_number': 5},
                    ]
                elif course_data['subject'] == 'English':
                    chapters_data = [
                        {'title': 'Learning Together', 'chapter_number': 1},
                        {'title': 'Wit and Humour', 'chapter_number': 2},
                        {'title': 'Dreams and Discoveries', 'chapter_number': 3},
                        {'title': 'Travel and Adventure', 'chapter_number': 4},
                        {'title': 'Brave Hearts', 'chapter_number': 5},
                    ]
                elif course_data['subject'] == 'Social Studies':
                    chapters_data = [
                        {'title': 'Trace Changes', 'chapter_number': 1},
                        {'title': 'Kingdoms', 'chapter_number': 2},
                        {'title': 'Sultans', 'chapter_number': 3},
                        {'title': 'Mughals', 'chapter_number': 4},
                        {'title': 'Rulers', 'chapter_number': 5},
                    ]
                elif course_data['subject'] == 'Computer Science':
                    chapters_data = [
                        {'title': 'Microsoft Word', 'chapter_number': 1},
                        {'title': 'Text Editing', 'chapter_number': 2},
                        {'title': 'MS Word Pictures', 'chapter_number': 3},
                        {'title': 'MS Word Smart Art', 'chapter_number': 4},
                        {'title': 'Smart Art Editing', 'chapter_number': 5},
                    ]

                for chapter_data in chapters_data:
                    chapter, created = Chapter.objects.get_or_create(
                        course=course,
                        chapter_number=chapter_data['chapter_number'],
                        defaults={
                            'title': chapter_data['title'],
                            'order': chapter_data['chapter_number'],
                            'is_published': True
                        }
                    )
                    if created:
                        self.stdout.write(f'  Created chapter: {chapter.title}')

                        # Create lessons for each chapter
                        for i in range(1, 4):  # 3 lessons per chapter
                            lesson, created = Lesson.objects.get_or_create(
                                chapter=chapter,
                                order=i,
                                defaults={
                                    'title': f'Lesson {i}: {chapter.title} - Part {i}',
                                    'description': f'Detailed lesson on {chapter.title} concepts',
                                    'lesson_type': 'video',
                                    'duration_minutes': 30,
                                    'is_published': True
                                }
                            )
                            if created:
                                self.stdout.write(f'    Created lesson: {lesson.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial data!')
        )
