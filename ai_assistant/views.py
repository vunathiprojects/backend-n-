from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json
import uuid
from datetime import datetime

from .models import (
    AIStudyPlan, AIGeneratedNote, ManualNote, 
    AIChatHistory, AIInteractionSession, AIFavorite
)
from .serializers import (
    AIStudyPlanSerializer, AIGeneratedNoteSerializer, ManualNoteSerializer,
    AIChatHistorySerializer, AIInteractionSessionSerializer, AIFavoriteSerializer
)
from authentication.models import User


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_ai_study_plan(request):
    """
    Save AI-generated study plan to database
    """
    try:
        data = request.data.copy()
        data['student_id'] = request.user.userid
        
        # Sanitize and validate data
        data['class_name'] = data.get('class_name', '').strip()
        data['subject'] = data.get('subject', '').strip()
        data['chapter'] = data.get('chapter', '').strip()
        data['subtopic'] = data.get('subtopic', '').strip() if data.get('subtopic') else ''
        data['plan_title'] = data.get('plan_title', '').strip()
        data['plan_content'] = data.get('plan_content', '').strip()
        data['plan_type'] = data.get('plan_type', 'study_plan').strip()
        data['difficulty_level'] = data.get('difficulty_level', 'medium').strip()
        
        # Handle undefined/null values
        if not data['class_name'] or data['class_name'] == 'undefined' or data['class_name'] == 'Class undefined':
            data['class_name'] = 'Unknown Class'
        if not data['subject'] or data['subject'] == 'undefined':
            data['subject'] = 'Unknown Subject'
        if not data['chapter'] or data['chapter'] == 'undefined':
            data['chapter'] = 'Unknown Chapter'
        if not data['plan_title'] or data['plan_title'] == 'undefined':
            data['plan_title'] = 'Study Plan'
        if not data['plan_content'] or data['plan_content'] == 'undefined':
            data['plan_content'] = 'No content available'
        
        # Ensure numeric fields are valid
        try:
            data['estimated_duration_hours'] = int(data.get('estimated_duration_hours', 1))
        except (ValueError, TypeError):
            data['estimated_duration_hours'] = 1
        
        # Check for duplicate content to avoid saving the same study plan multiple times
        existing_plan = AIStudyPlan.objects.filter(
            student_id=data['student_id'],
            class_name=data['class_name'],
            subject=data['subject'],
            chapter=data['chapter'],
            plan_content=data['plan_content']
        ).first()
        
        if existing_plan:
            return Response({
                'message': 'Study plan already exists',
                'study_plan': AIStudyPlanSerializer(existing_plan).data
            }, status=status.HTTP_200_OK)
        
        serializer = AIStudyPlanSerializer(data=data)
        if serializer.is_valid():
            study_plan = serializer.save()
            return Response({
                'message': 'Study plan saved successfully',
                'study_plan': AIStudyPlanSerializer(study_plan).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Failed to save study plan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_ai_generated_note(request):
    """
    Save AI-generated note to database
    """
    try:
        data = request.data.copy()
        data['student_id'] = request.user.userid
        
        # Sanitize and validate data
        data['class_name'] = data.get('class_name', '').strip()
        data['subject'] = data.get('subject', '').strip()
        data['chapter'] = data.get('chapter', '').strip()
        data['subtopic'] = data.get('subtopic', '').strip() if data.get('subtopic') else ''
        data['note_title'] = data.get('note_title', '').strip()
        data['note_content'] = data.get('note_content', '').strip()
        data['note_type'] = data.get('note_type', 'ai_generated').strip()
        
        # Handle undefined/null values
        if not data['class_name'] or data['class_name'] == 'undefined' or data['class_name'] == 'Class undefined':
            data['class_name'] = 'Unknown Class'
        if not data['subject'] or data['subject'] == 'undefined':
            data['subject'] = 'Unknown Subject'
        if not data['chapter'] or data['chapter'] == 'undefined':
            data['chapter'] = 'Unknown Chapter'
        if not data['note_title'] or data['note_title'] == 'undefined':
            data['note_title'] = 'AI Generated Notes'
        if not data['note_content'] or data['note_content'] == 'undefined':
            data['note_content'] = 'No content available'
        
        # Check for duplicate content to avoid saving the same note multiple times
        existing_note = AIGeneratedNote.objects.filter(
            student_id=data['student_id'],
            class_name=data['class_name'],
            subject=data['subject'],
            chapter=data['chapter'],
            note_content=data['note_content']
        ).first()
        
        if existing_note:
            return Response({
                'message': 'AI note already exists',
                'note': AIGeneratedNoteSerializer(existing_note).data
            }, status=status.HTTP_200_OK)
        
        serializer = AIGeneratedNoteSerializer(data=data)
        if serializer.is_valid():
            note = serializer.save()
            return Response({
                'message': 'AI note saved successfully',
                'note': AIGeneratedNoteSerializer(note).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Failed to save AI note: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_manual_note(request):
    """
    Save manual note to database
    """
    try:
        data = request.data.copy()
        data['student_id'] = request.user.userid
        
        # Sanitize and validate data
        data['class_name'] = data.get('class_name', '').strip()
        data['subject'] = data.get('subject', '').strip()
        data['chapter'] = data.get('chapter', '').strip()
        data['subtopic'] = data.get('subtopic', '').strip() if data.get('subtopic') else ''
        data['note_title'] = data.get('note_title', '').strip() if data.get('note_title') else ''
        data['note_content'] = data.get('note_content', '').strip()
        data['note_type'] = data.get('note_type', 'manual').strip()
        data['color'] = data.get('color', '#fef3c7').strip()
        
        # Handle undefined/null values
        if not data['class_name'] or data['class_name'] == 'undefined' or data['class_name'] == 'Class undefined':
            data['class_name'] = 'Unknown Class'
        if not data['subject'] or data['subject'] == 'undefined':
            data['subject'] = 'Unknown Subject'
        if not data['chapter'] or data['chapter'] == 'undefined':
            data['chapter'] = 'Unknown Chapter'
        if not data['note_content'] or data['note_content'] == 'undefined':
            data['note_content'] = 'No content available'
        if not data['color'] or data['color'] == 'undefined':
            data['color'] = '#fef3c7'
        
        # Ensure boolean fields are valid
        data['is_important'] = bool(data.get('is_important', False))
        
        serializer = ManualNoteSerializer(data=data)
        if serializer.is_valid():
            note = serializer.save()
            return Response({
                'message': 'Manual note saved successfully',
                'note': ManualNoteSerializer(note).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Failed to save manual note: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_chat_message(request):
    """
    Save AI chat message to database
    """
    try:
        data = request.data.copy()
        data['student_id'] = request.user.userid
        
        # Sanitize and validate data
        data['class_name'] = data.get('class_name', '').strip()
        data['subject'] = data.get('subject', '').strip()
        data['chapter'] = data.get('chapter', '').strip()
        data['subtopic'] = data.get('subtopic', '').strip() if data.get('subtopic') else ''
        data['user_message'] = data.get('user_message', '').strip()
        data['ai_response'] = data.get('ai_response', '').strip()
        data['response_type'] = data.get('response_type', 'general').strip()
        
        # Handle undefined/null values
        if not data['class_name'] or data['class_name'] == 'undefined' or data['class_name'] == 'Class undefined':
            data['class_name'] = 'Unknown Class'
        if not data['subject'] or data['subject'] == 'undefined':
            data['subject'] = 'Unknown Subject'
        if not data['chapter'] or data['chapter'] == 'undefined':
            data['chapter'] = 'Unknown Chapter'
        if not data['user_message'] or data['user_message'] == 'undefined':
            data['user_message'] = 'No message'
        if not data['ai_response'] or data['ai_response'] == 'undefined':
            data['ai_response'] = 'No response'
        
        # Generate session_id if not provided
        if not data.get('session_id'):
            data['session_id'] = str(uuid.uuid4())
        
        # Ensure boolean fields are valid
        data['is_favorite'] = bool(data.get('is_favorite', False))
        
        serializer = AIChatHistorySerializer(data=data)
        if serializer.is_valid():
            chat_message = serializer.save()
            return Response({
                'message': 'Chat message saved successfully',
                'chat_message': AIChatHistorySerializer(chat_message).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Failed to save chat message: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_study_plans(request):
    """
    Get study plans for the current user
    """
    try:
        class_name = request.GET.get('class_name')
        subject = request.GET.get('subject')
        chapter = request.GET.get('chapter')
        
        student_id = request.user.userid
        queryset = AIStudyPlan.objects.filter(student_id=student_id)
        
        if class_name:
            queryset = queryset.filter(class_name=class_name)
        if subject:
            queryset = queryset.filter(subject=subject)
        if chapter:
            queryset = queryset.filter(chapter=chapter)
        
        queryset = queryset.order_by('-created_at')
        
        serializer = AIStudyPlanSerializer(queryset, many=True)
        return Response({
            'study_plans': serializer.data
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to get study plans: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_ai_notes(request):
    """
    Get AI-generated notes for the current user
    """
    try:
        class_name = request.GET.get('class_name')
        subject = request.GET.get('subject')
        chapter = request.GET.get('chapter')
        
        student_id = request.user.userid
        queryset = AIGeneratedNote.objects.filter(student_id=student_id)
        
        if class_name:
            queryset = queryset.filter(class_name=class_name)
        if subject:
            queryset = queryset.filter(subject=subject)
        if chapter:
            queryset = queryset.filter(chapter=chapter)
        
        queryset = queryset.order_by('-created_at')
        
        serializer = AIGeneratedNoteSerializer(queryset, many=True)
        return Response({
            'ai_notes': serializer.data
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to get AI notes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_manual_notes(request):
    """
    Get manual notes for the current user
    """
    try:
        class_name = request.GET.get('class_name')
        subject = request.GET.get('subject')
        chapter = request.GET.get('chapter')
        
        student_id = request.user.userid
        queryset = ManualNote.objects.filter(student_id=student_id)
        
        if class_name:
            queryset = queryset.filter(class_name=class_name)
        if subject:
            queryset = queryset.filter(subject=subject)
        if chapter:
            queryset = queryset.filter(chapter=chapter)
        
        queryset = queryset.order_by('-created_at')
        
        serializer = ManualNoteSerializer(queryset, many=True)
        return Response({
            'manual_notes': serializer.data
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to get manual notes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_chat_history(request):
    """
    Get chat history for the current user
    """
    try:
        class_name = request.GET.get('class_name')
        subject = request.GET.get('subject')
        chapter = request.GET.get('chapter')
        session_id = request.GET.get('session_id')
        
        student_id = request.user.userid
        queryset = AIChatHistory.objects.filter(student_id=student_id)
        
        if class_name:
            queryset = queryset.filter(class_name=class_name)
        if subject:
            queryset = queryset.filter(subject=subject)
        if chapter:
            queryset = queryset.filter(chapter=chapter)
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        queryset = queryset.order_by('-message_timestamp')
        
        serializer = AIChatHistorySerializer(queryset, many=True)
        return Response({
            'chat_history': serializer.data
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to get chat history: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_manual_note(request, note_id):
    """
    Update a manual note
    """
    try:
        student_id = request.user.userid
        note = get_object_or_404(ManualNote, note_id=note_id, student_id=student_id)
        
        data = request.data.copy()
        
        # Sanitize and validate data
        if 'note_content' in data:
            data['note_content'] = data['note_content'].strip()
            if not data['note_content'] or data['note_content'] == 'undefined':
                data['note_content'] = 'No content available'
        
        if 'color' in data:
            data['color'] = data['color'].strip()
            if not data['color'] or data['color'] == 'undefined':
                data['color'] = '#fef3c7'
        
        if 'note_type' in data:
            data['note_type'] = data['note_type'].strip()
        
        # Ensure boolean fields are valid
        if 'is_important' in data:
            data['is_important'] = bool(data['is_important'])
        
        serializer = ManualNoteSerializer(note, data=data, partial=True)
        if serializer.is_valid():
            updated_note = serializer.save()
            return Response({
                'message': 'Note updated successfully',
                'note': ManualNoteSerializer(updated_note).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Failed to update note: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_manual_note(request, note_id):
    """
    Delete a manual note
    """
    try:
        student_id = request.user.userid
        note = get_object_or_404(ManualNote, note_id=note_id, student_id=student_id)
        note.delete()
        
        return Response({
            'message': 'Note deleted successfully'
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to delete note: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request):
    """
    Toggle favorite status for AI content
    """
    try:
        content_type = request.data.get('content_type')
        content_id = request.data.get('content_id')
        favorite_title = request.data.get('favorite_title', '')
        
        if not content_type or not content_id:
            return Response({
                'error': 'content_type and content_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if favorite already exists
        student_id = request.user.userid
        favorite, created = AIFavorite.objects.get_or_create(
            student_id=student_id,
            content_type=content_type,
            content_id=content_id,
            defaults={'favorite_title': favorite_title}
        )
        
        if not created:
            # Toggle favorite status by deleting it
            favorite.delete()
            return Response({
                'message': 'Removed from favorites',
                'is_favorite': False
            })
        else:
            return Response({
                'message': 'Added to favorites',
                'is_favorite': True,
                'favorite': AIFavoriteSerializer(favorite).data
            })
    
    except Exception as e:
        return Response({
            'error': f'Failed to toggle favorite: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_favorites(request):
    """
    Get all favorites for the current user
    """
    try:
        student_id = request.user.userid
        queryset = AIFavorite.objects.filter(student_id=student_id).order_by('-created_at')
        serializer = AIFavoriteSerializer(queryset, many=True)
        
        return Response({
            'favorites': serializer.data
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to get favorites: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_notes(request):
    """
    Get all notes (AI-generated and manual) for the current user
    """
    try:
        class_name = request.GET.get('class_name')
        subject = request.GET.get('subject')
        chapter = request.GET.get('chapter')
        
        # Get AI notes
        student_id = request.user.userid
        ai_queryset = AIGeneratedNote.objects.filter(student_id=student_id)
        if class_name:
            ai_queryset = ai_queryset.filter(class_name=class_name)
        if subject:
            ai_queryset = ai_queryset.filter(subject=subject)
        if chapter:
            ai_queryset = ai_queryset.filter(chapter=chapter)
        
        # Get manual notes
        manual_queryset = ManualNote.objects.filter(student_id=student_id)
        if class_name:
            manual_queryset = manual_queryset.filter(class_name=class_name)
        if subject:
            manual_queryset = manual_queryset.filter(subject=subject)
        if chapter:
            manual_queryset = manual_queryset.filter(chapter=chapter)
        
        ai_notes = AIGeneratedNoteSerializer(ai_queryset.order_by('-created_at'), many=True).data
        manual_notes = ManualNoteSerializer(manual_queryset.order_by('-created_at'), many=True).data
        
        # Combine and sort by creation date
        all_notes = []
        for note in ai_notes:
            note['note_type'] = 'ai_generated'
            all_notes.append(note)
        
        for note in manual_notes:
            note['note_type'] = 'manual'
            all_notes.append(note)
        
        # Sort by created_at
        all_notes.sort(key=lambda x: x['created_at'], reverse=True)
        
        return Response({
            'all_notes': all_notes,
            'ai_notes_count': len(ai_notes),
            'manual_notes_count': len(manual_notes)
        })
    
    except Exception as e:
        return Response({
            'error': f'Failed to get all notes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
