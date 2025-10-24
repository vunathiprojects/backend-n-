"""
Static Quiz Views for 7th Class Subjects
These views serve pre-defined quiz data without requiring database storage
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
import json

from .static_quiz_data import (
    get_quiz_data, get_all_subjects, get_topics_for_subject,
    get_questions_for_topic, calculate_quiz_score, STATIC_QUIZZES
)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_static_subjects(request):
    """
    Get all available subjects for static quizzes
    """
    try:
        subjects = []
        for subject_key, subject_data in STATIC_QUIZZES.items():
            subjects.append({
                'subject_key': subject_key,
                'subject_name': subject_data['subject_name'],
                'class': subject_data['class'],
                'topics_count': len(subject_data['topics'])
            })
        
        return Response({
            'subjects': subjects,
            'total_subjects': len(subjects)
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch subjects: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_static_topics(request, subject):
    """
    Get all topics for a specific subject
    """
    try:
        topics = get_topics_for_subject(subject)
        if not topics:
            return Response(
                {'error': f'No topics found for subject: {subject}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        topic_list = []
        for topic_key in topics:
            topic_data = get_quiz_data(subject, topic_key)
            topic_list.append({
                'topic_key': topic_key,
                'topic_name': topic_data['topic_name'],
                'description': topic_data['description'],
                'questions_count': len(topic_data['questions'])
            })
        
        return Response({
            'subject': subject,
            'topics': topic_list,
            'total_topics': len(topic_list)
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch topics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_static_quiz(request, subject, topic):
    """
    Get quiz questions for a specific topic
    """
    try:
        questions = get_questions_for_topic(subject, topic)
        if not questions:
            return Response(
                {'error': f'No questions found for {subject} - {topic}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get topic information
        topic_data = get_quiz_data(subject, topic)
        
        # Format questions for frontend
        formatted_questions = []
        for question in questions:
            formatted_question = {
                'question_id': question['question_id'],
                'question_text': question['question_text'],
                'question_type': question['question_type'],
                'points': question['points'],
                'options': [
                    {
                        'option_id': option['option_id'],
                        'option_text': option['option_text']
                    }
                    for option in question['options']
                ]
            }
            formatted_questions.append(formatted_question)
        
        return Response({
            'subject': subject,
            'topic': topic,
            'topic_name': topic_data['topic_name'],
            'description': topic_data['description'],
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'total_points': sum(q['points'] for q in questions)
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch quiz: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_static_quiz(request, subject, topic):
    """
    Submit quiz answers and get results
    """
    try:
        answers = request.data.get('answers', [])
        if not answers:
            return Response(
                {'error': 'No answers provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate score
        score_info = calculate_quiz_score(answers)
        
        # Get detailed results
        detailed_results = []
        questions = get_questions_for_topic(subject, topic)
        
        # Create a lookup for questions
        question_lookup = {q['question_id']: q for q in questions}
        
        for answer in answers:
            question_id = answer.get('question_id')
            selected_option = answer.get('selected_option')
            
            if question_id in question_lookup:
                question = question_lookup[question_id]
                
                # Find correct option
                correct_option = None
                for option in question['options']:
                    if option['is_correct']:
                        correct_option = option['option_id']
                        break
                
                is_correct = selected_option == correct_option
                
                detailed_results.append({
                    'question_id': question_id,
                    'question_text': question['question_text'],
                    'selected_option': selected_option,
                    'correct_option': correct_option,
                    'is_correct': is_correct,
                    'points_earned': question['points'] if is_correct else 0,
                    'explanation': question.get('explanation', '')
                })
        
        return Response({
            'subject': subject,
            'topic': topic,
            'user_id': request.user.userid,
            'username': request.user.username,
            'score_info': score_info,
            'detailed_results': detailed_results,
            'submitted_at': request.data.get('submitted_at')
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to submit quiz: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_static_quiz_preview(request, subject, topic):
    """
    Get a preview of quiz questions (without answers) for practice
    """
    try:
        questions = get_questions_for_topic(subject, topic)
        if not questions:
            return Response(
                {'error': f'No questions found for {subject} - {topic}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get topic information
        topic_data = get_quiz_data(subject, topic)
        
        # Return only question structure without correct answers
        preview_questions = []
        for question in questions:
            preview_question = {
                'question_id': question['question_id'],
                'question_text': question['question_text'],
                'question_type': question['question_type'],
                'points': question['points'],
                'options': [
                    {
                        'option_id': option['option_id'],
                        'option_text': option['option_text']
                    }
                    for option in question['options']
                ]
            }
            preview_questions.append(preview_question)
        
        return Response({
            'subject': subject,
            'topic': topic,
            'topic_name': topic_data['topic_name'],
            'description': topic_data['description'],
            'questions': preview_questions,
            'total_questions': len(preview_questions),
            'total_points': sum(q['points'] for q in questions),
            'estimated_time_minutes': len(questions) * 2  # 2 minutes per question
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch quiz preview: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_static_quiz_statistics(request):
    """
    Get statistics about available static quizzes
    """
    try:
        stats = {
            'total_subjects': len(STATIC_QUIZZES),
            'total_topics': 0,
            'total_questions': 0,
            'subjects': []
        }
        
        for subject_key, subject_data in STATIC_QUIZZES.items():
            subject_stats = {
                'subject_key': subject_key,
                'subject_name': subject_data['subject_name'],
                'class': subject_data['class'],
                'topics_count': len(subject_data['topics']),
                'questions_count': 0,
                'topics': []
            }
            
            for topic_key, topic_data in subject_data['topics'].items():
                questions_count = len(topic_data['questions'])
                subject_stats['questions_count'] += questions_count
                subject_stats['topics'].append({
                    'topic_key': topic_key,
                    'topic_name': topic_data['topic_name'],
                    'questions_count': questions_count
                })
            
            stats['total_topics'] += subject_stats['topics_count']
            stats['total_questions'] += subject_stats['questions_count']
            stats['subjects'].append(subject_stats)
        
        return Response(stats)
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch statistics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_static_quiz_help(request):
    """
    Get help information about static quizzes
    """
    help_info = {
        'title': 'Static Quiz System Help',
        'description': 'Interactive quiz system for 7th class Mathematics and Science subjects',
        'features': [
            'Multiple choice questions with immediate feedback',
            'Topic-wise quiz organization',
            'Automatic score calculation',
            'Detailed explanations for each answer',
            'Progress tracking and statistics'
        ],
        'subjects_available': list(STATIC_QUIZZES.keys()),
        'how_to_use': [
            '1. Select a subject (Mathematics or Science)',
            '2. Choose a topic from the available topics',
            '3. Start the quiz and answer questions',
            '4. Submit your answers to get results',
            '5. Review explanations for better understanding'
        ],
        'scoring_system': {
            'passing_percentage': 60,
            'points_per_question': 'Varies (1-2 points)',
            'total_score': 'Sum of all question points'
        },
        'api_endpoints': {
            'subjects': '/api/quizzes/static/subjects/',
            'topics': '/api/quizzes/static/subjects/{subject}/topics/',
            'quiz': '/api/quizzes/static/subjects/{subject}/topics/{topic}/',
            'submit': '/api/quizzes/static/subjects/{subject}/topics/{topic}/submit/',
            'preview': '/api/quizzes/static/subjects/{subject}/topics/{topic}/preview/',
            'statistics': '/api/quizzes/static/statistics/'
        }
    }
    
    return Response(help_info)
