"""
PDF Quiz Views - Serve PDF-based quizzes organized by class/subject/topic/chapter
This system integrates with the existing frontend quiz section
"""

import os
import json
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .pdf_question_extractor import get_all_pdf_questions, extract_questions_from_pdf

# PDF structure mapping based on frontend topic names from Quizzes.jsx
PDF_STRUCTURE = {
    "class7": {
        "name": "Class 7",
        "subjects": {
            "maths": {
                "name": "Mathematics",
                "topics": {
                    "chapter1_integers": {"name": "Chapter 1 Integers", "file": "Chapter 1 Integers (Properties of Addition and Subtraction of Integers).pdf"},
                    "lines_and_angles": {"name": "Lines and Angles", "file": "maths_lines_and_angles_quiz.pdf"},
                    "fractions": {"name": "Fractions", "file": "maths_fractions_quiz.pdf"}
                }
            },
            "science": {
                "name": "Science",
                "topics": {
                    "electricity": {"name": "Electricity", "file": "science_electricity_quiz.pdf"},
                    "metals_and_non_metals": {"name": "Metals and Non-Metals", "file": "science_metals_and_non_metals_quiz.pdf"},
                    "human_biology": {"name": "Human Biology", "file": "science_human_biology_quiz.pdf"}
                }
            },
            "english": {
                "name": "English",
                "topics": {
                    "nutrition_in_animals": {"name": "Nutrition in Animals", "file": "english_nutrition_in_animals_quiz.pdf"},
                    "grammar": {"name": "Grammar", "file": "english_grammar_quiz.pdf"}
                }
            },
            "social": {
                "name": "Social Studies",
                "topics": {
                    "indian_history": {"name": "Indian History", "file": "social_indian_history_quiz.pdf"},
                    "world_geography": {"name": "World Geography", "file": "social_world_geography_quiz.pdf"}
                }
            },
            "computer": {
                "name": "Computer Science",
                "topics": {
                    # Programming Language subtopics
                    "programming_language_basics": {"name": "What is a programming language", "file": "Unit-1 Programming Language (1.1  What is a programming language ).pdf"},
                    "programming_language_types": {"name": "Types Low-level vs High-level languages", "file": "Unit-1 Programming Language ( 1.2Types Low-level vs High-level languages).pdf"},
                    "programming_language_examples": {"name": "Examples and real-world uses", "file": "Unit-1 Programming Language (1.3 Examples and real-world uses).pdf"},
                    "programming_language_logic": {"name": "Simple pseudocode or introduction to programming logic", "file": "Unit-1 Programming Language ( 1.4Simple pseudocode or introduction to programming logic).pdf"},
                    
                    # Microsoft Word subtopics
                    "microsoft_word_documents": {"name": "Creating, saving, and opening documents", "file": "Unit-2. Editing Text in Microsoft Word (2.1 Creating, saving, and opening documents ).pdf"},
                    "microsoft_word_formatting": {"name": "Text formatting fonts, sizes, colors, bold, italics", "file": "Unit-2. Editing Text in Microsoft Word (2.2 Text formatting fonts, sizes, colors, bold, italics).pdf"},
                    "microsoft_word_paragraphs": {"name": "Paragraph alignment, bullets, numbering", "file": "Unit-2. Editing Text in Microsoft Word (2.3 Paragraph alignment, bullets, numbering ).pdf"},
                    "microsoft_word_inserting": {"name": "Inserting images, tables, and hyperlinks", "file": "Unit-2. Editing Text in Microsoft Word (2.4 Inserting images, tables, and hyperlinks).pdf"},
                    
                    # Microsoft PowerPoint subtopics
                    "microsoft_powerpoint_slides": {"name": "Creating slides and using slide layouts", "file": "Unit-3. Microsoft PowerPoint (3.1  Creating slides and using slide layouts ).pdf"},
                    "microsoft_powerpoint_text_images": {"name": "Adding and editing text and images", "file": "Unit-3. Microsoft PowerPoint (3.2 Adding and editing text and images ).pdf"},
                    "microsoft_powerpoint_themes": {"name": "Applying themes and transitions", "file": "Unit-3. Microsoft PowerPoint (3.3  Applying themes and transitions ).pdf"},
                    "microsoft_powerpoint_slideshow": {"name": "Running a slideshow", "file": "Unit-3. Microsoft PowerPoint (3.4 Running a slideshow ).pdf"},
                    
                    # Microsoft Excel subtopics
                    "microsoft_excel_data": {"name": "Entering and formatting data in cells", "file": "Unit-4. Basics of Microsoft Excel (4.1 Entering and formatting data in cells ).pdf"},
                    "microsoft_excel_formulas": {"name": "Basic formulas (SUM, AVERAGE)", "file": "Unit-4. Basics of Microsoft Excel (4.2 Basic formulas (SUM, AVERAGE) ).pdf"},
                    "microsoft_excel_charts": {"name": "Creating charts from data", "file": "Unit-4. Basics of Microsoft Excel (4.3 Creating charts from data ).pdf"},
                    "microsoft_excel_organization": {"name": "Simple data organization (sorting and filtering)", "file": "Unit-4. Basics of Microsoft Excel (4.4 Simple data organization (sorting and filtering) ).pdf"},
                    
                    # Microsoft Access subtopics
                    "microsoft_access_tables": {"name": "Understanding databases and tables", "file": "Unit-5. Microsoft Access (5.1 Understanding databases and tables ).pdf"},
                    "microsoft_access_database": {"name": "Creating a simple database", "file": "Unit-5. Microsoft Access (5.2  Creating a simple database ).pdf"},
                    "microsoft_access_records": {"name": "Adding, editing, and searching records", "file": "Unit-5. Microsoft Access (5.3 Adding, editing, and searching records ).pdf"},
                    "microsoft_access_queries": {"name": "Basic queries", "file": "Unit-5. Microsoft Access (5.4  Basic queries ).pdf"},
                    
                    # Backward compatibility - keep old topic endpoints for frontend
                    "programming_language": {"name": "Programming Language", "file": "Unit-1 Programming Language (1.1  What is a programming language ).pdf"},
                    "microsoft_word": {"name": "Microsoft Word", "file": "Unit-2. Editing Text in Microsoft Word (2.1 Creating, saving, and opening documents ).pdf"},
                    "microsoft_powerpoint": {"name": "Microsoft PowerPoint", "file": "Unit-3. Microsoft PowerPoint (3.1  Creating slides and using slide layouts ).pdf"},
                    "microsoft_excel": {"name": "Microsoft Excel", "file": "Unit-4. Basics of Microsoft Excel (4.1 Entering and formatting data in cells ).pdf"},
                    "microsoft_access": {"name": "Microsoft Access", "file": "Unit-5. Microsoft Access (5.1 Understanding databases and tables ).pdf"}
                }
            }
        }
    },
    "class8": {
        "name": "Class 8",
        "subjects": {
            "maths": {
                "name": "Mathematics",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "science": {
                "name": "Science",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "english": {
                "name": "English",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "social": {
                "name": "Social Studies",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "computer": {
                "name": "Computer Science",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            }
        }
    },
    "class9": {
        "name": "Class 9",
        "subjects": {
            "maths": {
                "name": "Mathematics",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "science": {
                "name": "Science",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "english": {
                "name": "English",
                "topics": {
                    "lesson1": {"name": "Lesson 1", "file": "lesson-1.pdf"},
                    "lesson2": {"name": "Lesson 2", "file": "lesson-2.pdf"},
                    "lesson3": {"name": "Lesson 3", "file": "lesson-3.pdf"},
                    "lesson4": {"name": "Lesson 4", "file": "lesson-4.pdf"},
                    "lesson5": {"name": "Lesson 5", "file": "lesson-5.pdf"}
                }
            },
            "social": {
                "name": "Social Studies",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "computer": {
                "name": "Computer Science",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            }
        }
    },
    "class10": {
        "name": "Class 10",
        "subjects": {
            "maths": {
                "name": "Mathematics",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "science": {
                "name": "Science",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "english": {
                "name": "English",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "social": {
                "name": "Social Studies",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            },
            "computer": {
                "name": "Computer Science",
                "topics": {
                    "chapter1": {"name": "Chapter 1", "file": "chapter1.pdf"},
                    "chapter2": {"name": "Chapter 2", "file": "chapter2.pdf"},
                    "chapter3": {"name": "Chapter 3", "file": "chapter3.pdf"},
                    "chapter4": {"name": "Chapter 4", "file": "chapter4.pdf"},
                    "chapter5": {"name": "Chapter 5", "file": "chapter5.pdf"}
                }
            }
        }
    }
}

def get_pdf_path(class_name, subject, topic_key):
    """Get the full path to a PDF file"""
    try:
        topic_info = PDF_STRUCTURE[class_name]["subjects"][subject]["topics"][topic_key]
        filename = topic_info["file"]
        
        # Construct the path to quiz PDFs in backend media folder
        pdf_path = os.path.join(settings.BASE_DIR, 'media', 'quiz_pdfs', class_name, subject, filename)
        
        return pdf_path
    except KeyError:
        return None

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pdf_quiz_structure(request):
    """
    Get the complete PDF quiz structure organized by class/subject/topic
    """
    try:
        # Format the structure for frontend consumption
        formatted_structure = {}
        
        for class_key, class_data in PDF_STRUCTURE.items():
            formatted_structure[class_key] = {
                "name": class_data["name"],
                "subjects": {}
            }
            
            for subject_key, subject_data in class_data["subjects"].items():
                formatted_structure[class_key]["subjects"][subject_key] = {
                    "name": subject_data["name"],
                    "topics": {}
                }
                
                for topic_key, topic_data in subject_data["topics"].items():
                    formatted_structure[class_key]["subjects"][subject_key]["topics"][topic_key] = {
                        "name": topic_data["name"],
                        "file": topic_data["file"],
                        "available": os.path.exists(get_pdf_path(class_key, subject_key, topic_key))
                    }
        
        return Response({
            "structure": formatted_structure,
            "total_classes": len(PDF_STRUCTURE),
            "total_subjects": sum(len(class_data["subjects"]) for class_data in PDF_STRUCTURE.values()),
            "total_topics": sum(
                len(subject_data["topics"]) 
                for class_data in PDF_STRUCTURE.values() 
                for subject_data in class_data["subjects"].values()
            )
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch PDF structure: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pdf_quiz_subjects(request, class_name):
    """
    Get all subjects for a specific class
    """
    try:
        if class_name not in PDF_STRUCTURE:
            return Response(
                {'error': f'Class {class_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        class_data = PDF_STRUCTURE[class_name]
        subjects = []
        
        for subject_key, subject_data in class_data["subjects"].items():
            subjects.append({
                "key": subject_key,
                "name": subject_data["name"],
                "topics_count": len(subject_data["topics"])
            })
        
        return Response({
            "class": class_name,
            "class_name": class_data["name"],
            "subjects": subjects,
            "total_subjects": len(subjects)
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch subjects: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pdf_quiz_topics(request, class_name, subject):
    """
    Get all topics for a specific class and subject
    """
    try:
        if class_name not in PDF_STRUCTURE:
            return Response(
                {'error': f'Class {class_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response(
                {'error': f'Subject {subject} not found in {class_name}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        subject_data = PDF_STRUCTURE[class_name]["subjects"][subject]
        topics = []
        
        for topic_key, topic_data in subject_data["topics"].items():
            pdf_path = get_pdf_path(class_name, subject, topic_key)
            topics.append({
                "key": topic_key,
                "name": topic_data["name"],
                "file": topic_data["file"],
                "available": os.path.exists(pdf_path) if pdf_path else False
            })
        
        return Response({
            "class": class_name,
            "subject": subject,
            "subject_name": subject_data["name"],
            "topics": topics,
            "total_topics": len(topics)
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch topics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pdf_quiz_info(request, class_name, subject, topic):
    """
    Get information about a specific PDF quiz topic
    """
    try:
        if class_name not in PDF_STRUCTURE:
            return Response(
                {'error': f'Class {class_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response(
                {'error': f'Subject {subject} not found in {class_name}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if topic not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            return Response(
                {'error': f'Topic {topic} not found in {subject}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        topic_data = PDF_STRUCTURE[class_name]["subjects"][subject]["topics"][topic]
        pdf_path = get_pdf_path(class_name, subject, topic)
        
        # Check if PDF exists
        if not pdf_path or not os.path.exists(pdf_path):
            return Response(
                {'error': f'PDF file not found: {topic_data["file"]}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get file size
        file_size = os.path.getsize(pdf_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        return Response({
            "class": class_name,
            "subject": subject,
            "topic": topic,
            "topic_name": topic_data["name"],
            "file": topic_data["file"],
            "file_size_mb": file_size_mb,
            "available": True,
            "download_url": f"/api/quizzes/pdf/{class_name}/{subject}/{topic}/download/",
            "preview_url": f"/api/quizzes/pdf/{class_name}/{subject}/{topic}/preview/"
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch topic info: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_pdf_quiz(request, class_name, subject, topic):
    """
    Download a specific PDF quiz file
    """
    try:
        if class_name not in PDF_STRUCTURE:
            raise Http404("Class not found")
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            raise Http404("Subject not found")
        
        if topic not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            raise Http404("Topic not found")
        
        topic_data = PDF_STRUCTURE[class_name]["subjects"][subject]["topics"][topic]
        pdf_path = get_pdf_path(class_name, subject, topic)
        
        if not pdf_path or not os.path.exists(pdf_path):
            raise Http404("PDF file not found")
        
        # Return the PDF file
        response = FileResponse(
            open(pdf_path, 'rb'),
            content_type='application/pdf',
            filename=topic_data["file"]
        )
        response['Content-Disposition'] = f'attachment; filename="{topic_data["file"]}"'
        return response
    
    except Exception as e:
        return Response(
            {'error': f'Failed to download PDF: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pdf_quiz_for_frontend(request, class_name, subject, topic):
    """
    Get PDF quiz data formatted for the existing frontend quiz system
    This endpoint integrates with your existing Quizzes.jsx component
    """
    try:
        if class_name not in PDF_STRUCTURE:
            return Response(
                {'error': f'Class {class_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response(
                {'error': f'Subject {subject} not found in {class_name}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if topic not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            return Response(
                {'error': f'Topic {topic} not found in {subject}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        topic_data = PDF_STRUCTURE[class_name]["subjects"][subject]["topics"][topic]
        pdf_path = get_pdf_path(class_name, subject, topic)
        
        if not pdf_path or not os.path.exists(pdf_path):
            return Response(
                {'error': f'PDF file not found: {topic_data["file"]}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Format data to match your existing frontend structure
        quiz_data = {
            "id": f"{class_name}-{subject}-{topic}",
            "name": topic_data["name"],
            "lesson": PDF_STRUCTURE[class_name]["subjects"][subject]["name"],
            "class": PDF_STRUCTURE[class_name]["name"],
            "subject": subject,
            "topic": topic,
            "file": topic_data["file"],
            "download_url": f"/api/quizzes/pdf/{class_name}/{subject}/{topic}/download/",
            "type": "pdf_quiz",
            "description": f"PDF Quiz for {topic_data['name']} - {PDF_STRUCTURE[class_name]['subjects'][subject]['name']}",
            "instructions": [
                "This is a PDF-based quiz",
                "Download the PDF to view the questions",
                "Answer the questions in the PDF",
                "Submit your answers through the system"
            ]
        }
        
        return Response(quiz_data)
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch PDF quiz data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_pdf_quizzes(request):
    """
    Search PDF quizzes by class, subject, or topic name
    """
    try:
        query = request.GET.get('q', '').lower()
        class_filter = request.GET.get('class', '')
        subject_filter = request.GET.get('subject', '')
        
        results = []
        
        for class_key, class_data in PDF_STRUCTURE.items():
            # Apply class filter
            if class_filter and class_key != class_filter:
                continue
            
            for subject_key, subject_data in class_data["subjects"].items():
                # Apply subject filter
                if subject_filter and subject_key != subject_filter:
                    continue
                
                for topic_key, topic_data in subject_data["topics"].items():
                    # Search in topic name, subject name, and class name
                    searchable_text = f"{topic_data['name']} {subject_data['name']} {class_data['name']}".lower()
                    
                    if query in searchable_text:
                        pdf_path = get_pdf_path(class_key, subject_key, topic_key)
                        results.append({
                            "class": class_key,
                            "class_name": class_data["name"],
                            "subject": subject_key,
                            "subject_name": subject_data["name"],
                            "topic": topic_key,
                            "topic_name": topic_data["name"],
                            "file": topic_data["file"],
                            "available": os.path.exists(pdf_path) if pdf_path else False,
                            "download_url": f"/api/quizzes/pdf/{class_key}/{subject_key}/{topic_key}/download/"
                        })
        
        return Response({
            "query": query,
            "results": results,
            "total_results": len(results)
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to search PDF quizzes: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pdf_quiz_statistics(request):
    """
    Get statistics about available PDF quizzes
    """
    try:
        stats = {
            "total_classes": len(PDF_STRUCTURE),
            "total_subjects": 0,
            "total_topics": 0,
            "available_pdfs": 0,
            "classes": []
        }
        
        for class_key, class_data in PDF_STRUCTURE.items():
            class_stats = {
                "class": class_key,
                "class_name": class_data["name"],
                "subjects_count": len(class_data["subjects"]),
                "topics_count": 0,
                "available_pdfs": 0,
                "subjects": []
            }
            
            for subject_key, subject_data in class_data["subjects"].items():
                subject_stats = {
                    "subject": subject_key,
                    "subject_name": subject_data["name"],
                    "topics_count": len(subject_data["topics"]),
                    "available_pdfs": 0
                }
                
                for topic_key, topic_data in subject_data["topics"].items():
                    pdf_path = get_pdf_path(class_key, subject_key, topic_key)
                    if pdf_path and os.path.exists(pdf_path):
                        subject_stats["available_pdfs"] += 1
                        class_stats["available_pdfs"] += 1
                        stats["available_pdfs"] += 1
                
                subject_stats["topics_count"] = len(subject_data["topics"])
                class_stats["topics_count"] += subject_stats["topics_count"]
                stats["total_topics"] += subject_stats["topics_count"]
                
                class_stats["subjects"].append(subject_stats)
            
            stats["total_subjects"] += class_stats["subjects_count"]
            stats["classes"].append(class_stats)
        
        return Response(stats)
    
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch PDF statistics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily allow access without authentication for testing
def get_pdf_quiz_questions(request, class_name, subject, topic_key):
    """
    Get interactive quiz questions extracted from the specific PDF for this topic
    """
    try:
        print(f"🔍 Fetching questions for: {class_name}/{subject}/{topic_key}")
        
        # Validate the request parameters
        if class_name not in PDF_STRUCTURE:
            return Response({
                "error": f"Class '{class_name}' not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response({
                "error": f"Subject '{subject}' not found in class '{class_name}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if topic_key not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            return Response({
                "error": f"Topic '{topic_key}' not found in subject '{subject}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get the specific PDF path for this topic
        pdf_path = get_pdf_path(class_name, subject, topic_key)
        
        if not pdf_path or not os.path.exists(pdf_path):
            return Response({
                "error": f"PDF file not found for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        print(f"📄 Extracting questions from: {pdf_path}")
        
        # Extract questions from the specific PDF file
        questions = extract_questions_from_pdf(pdf_path)
        
        if not questions:
            return Response({
                "error": f"No questions could be extracted from PDF for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        topic_data = PDF_STRUCTURE[class_name]["subjects"][subject]["topics"][topic_key]
        
        print(f"✅ Successfully extracted {len(questions)} questions from {os.path.basename(pdf_path)}")
        
        return Response({
            "topic_name": topic_data["name"],
            "description": f"Interactive quiz questions from {topic_data['name']} ({len(questions)} questions)",
            "total_questions": len(questions),
            "total_points": sum(q.get("points", 1) for q in questions),
            "questions": questions,
            "pdf_file": os.path.basename(pdf_path)
        })
    
    except Exception as e:
        print(f"❌ Error fetching questions: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return Response({
            "error": f"Failed to get quiz questions: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Temporarily allow access without authentication for testing
def submit_pdf_quiz_answers(request, class_name, subject, topic_key):
    """
    Submit answers for PDF quiz questions
    """
    try:
        print(f"🔍 Submit request received for {class_name}/{subject}/{topic_key}")
        print(f"📝 Request data: {request.data}")
        
        # Validate the request parameters
        if class_name not in PDF_STRUCTURE:
            return Response({
                "error": f"Class '{class_name}' not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response({
                "error": f"Subject '{subject}' not found in class '{class_name}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if topic_key not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            return Response({
                "error": f"Topic '{topic_key}' not found in subject '{subject}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get the specific PDF path for this topic
        pdf_path = get_pdf_path(class_name, subject, topic_key)
        
        if not pdf_path or not os.path.exists(pdf_path):
            return Response({
                "error": f"PDF file not found for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Extract questions from the specific PDF file
        questions = extract_questions_from_pdf(pdf_path)
        
        if not questions:
            return Response({
                "error": f"No questions could be extracted from PDF for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Handle different data formats from frontend
        if hasattr(request, 'data') and request.data:
            answers = request.data.get('answers', [])
        else:
            # Fallback for different request formats
            import json
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                answers = body_data.get('answers', [])
            except:
                answers = []
        
        print(f"📊 Processing {len(answers)} answers for {len(questions)} questions")
        
        # Calculate score
        correct_answers = 0
        total_questions = len(questions)
        results = []
        
        for answer in answers:
            try:
                # Handle different answer formats
                if isinstance(answer, dict):
                    question_id = answer.get('question_id')
                    selected_option = answer.get('selected_option')
                else:
                    print(f"⚠️ Invalid answer format: {answer}")
                    continue
                
                # Convert question_id to int if it's a string
                if isinstance(question_id, str) and question_id.isdigit():
                    question_id = int(question_id)
                
                print(f"🔍 Processing answer: Q{question_id} = {selected_option}")
                
                # Find the question
                question = next((q for q in questions if q['id'] == question_id), None)
                if question:
                    is_correct = selected_option == question['correct_option']
                    if is_correct:
                        correct_answers += 1
                    
                    results.append({
                        "question_id": question_id,
                        "question_text": question['question_text'],
                        "selected_option": selected_option,
                        "correct_option": question['correct_option'],
                        "is_correct": is_correct,
                        "explanation": question['explanation']
                    })
                else:
                    print(f"⚠️ Question {question_id} not found")
            except Exception as e:
                print(f"⚠️ Error processing answer {answer}: {e}")
                continue
        
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        result_data = {
            "score": correct_answers,
            "total_questions": total_questions,
            "percentage": round(score_percentage, 1),
            "correct_answers": correct_answers,
            "wrong_answers": total_questions - correct_answers,
            "results": results
        }
        
        print(f"✅ Submit successful: {correct_answers}/{total_questions} correct ({score_percentage:.1f}%)")
        return Response(result_data)
    
    except Exception as e:
        print(f"❌ Submit error: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return Response({
            "error": f"Failed to submit quiz answers: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily allow access without authentication for testing
def get_maths_randomized_quiz(request, class_name, subject, topic_key):
    """
    Get randomized quiz questions for Maths subject
    Returns 10 random questions from the full question bank for each attempt
    """
    try:
        print(f"🔍 Fetching randomized Maths quiz for: {class_name}/{subject}/{topic_key}")
        
        # Validate the request parameters
        if class_name not in PDF_STRUCTURE:
            return Response({
                "error": f"Class '{class_name}' not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response({
                "error": f"Subject '{subject}' not found in class '{class_name}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if topic_key not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            return Response({
                "error": f"Topic '{topic_key}' not found in subject '{subject}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Only allow this endpoint for Maths subject
        if subject != "maths":
            return Response({
                "error": "This endpoint is only available for Maths subject"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the specific PDF path for this topic
        pdf_path = get_pdf_path(class_name, subject, topic_key)
        
        if not pdf_path or not os.path.exists(pdf_path):
            return Response({
                "error": f"PDF file not found for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        print(f"📄 Extracting questions from: {pdf_path}")
        
        # Extract ALL questions from the PDF file
        all_questions = extract_questions_from_pdf(pdf_path)
        
        if not all_questions:
            return Response({
                "error": f"No questions could be extracted from PDF for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        print(f"📊 Total questions in bank: {len(all_questions)}")
        
        # Randomize and select 10 questions
        import random
        random.shuffle(all_questions)  # Shuffle the questions
        selected_questions = all_questions[:10]  # Take first 10
        
        # Re-number the selected questions to start from 1
        for i, question in enumerate(selected_questions):
            question['id'] = i + 1
        
        topic_data = PDF_STRUCTURE[class_name]["subjects"][subject]["topics"][topic_key]
        
        print(f"✅ Returning {len(selected_questions)} randomized questions from {os.path.basename(pdf_path)}")
        
        return Response({
            "topic_name": topic_data["name"],
            "description": f"Randomized quiz from {topic_data['name']} - 10 questions selected from {len(all_questions)} total questions",
            "total_questions_in_bank": len(all_questions),
            "questions_displayed": len(selected_questions),
            "total_questions": len(selected_questions),
            "total_points": sum(q.get("points", 1) for q in selected_questions),
            "questions": selected_questions,
            "pdf_file": os.path.basename(pdf_path),
            "quiz_type": "randomized",
            "subject": "maths"
        })
    
    except Exception as e:
        print(f"❌ Error fetching randomized quiz: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return Response({
            "error": f"Failed to get randomized quiz questions: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Temporarily allow access without authentication for testing
def submit_maths_randomized_quiz_answers(request, class_name, subject, topic_key):
    """
    Submit answers for randomized Maths quiz questions
    """
    try:
        print(f"🔍 Submit randomized quiz request received for {class_name}/{subject}/{topic_key}")
        print(f"📝 Request data: {request.data}")
        
        # Validate the request parameters
        if class_name not in PDF_STRUCTURE:
            return Response({
                "error": f"Class '{class_name}' not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if subject not in PDF_STRUCTURE[class_name]["subjects"]:
            return Response({
                "error": f"Subject '{subject}' not found in class '{class_name}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if topic_key not in PDF_STRUCTURE[class_name]["subjects"][subject]["topics"]:
            return Response({
                "error": f"Topic '{topic_key}' not found in subject '{subject}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Only allow this endpoint for Maths subject
        if subject != "maths":
            return Response({
                "error": "This endpoint is only available for Maths subject"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the specific PDF path for this topic
        pdf_path = get_pdf_path(class_name, subject, topic_key)
        
        if not pdf_path or not os.path.exists(pdf_path):
            return Response({
                "error": f"PDF file not found for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Extract ALL questions from the PDF file to validate answers
        all_questions = extract_questions_from_pdf(pdf_path)
        
        if not all_questions:
            return Response({
                "error": f"No questions could be extracted from PDF for topic '{topic_key}'"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Handle different data formats from frontend
        if hasattr(request, 'data') and request.data:
            answers = request.data.get('answers', [])
        else:
            # Fallback for different request formats
            import json
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                answers = body_data.get('answers', [])
            except:
                answers = []
        
        print(f"📊 Processing {len(answers)} answers for randomized quiz")
        
        # Calculate score
        correct_answers = 0
        total_questions = len(answers)
        results = []
        
        for answer in answers:
            try:
                # Handle different answer formats
                if isinstance(answer, dict):
                    question_id = answer.get('question_id')
                    selected_option = answer.get('selected_option')
                else:
                    print(f"⚠️ Invalid answer format: {answer}")
                    continue
                
                # Convert question_id to int if it's a string
                if isinstance(question_id, str) and question_id.isdigit():
                    question_id = int(question_id)
                
                print(f"🔍 Processing answer: Q{question_id} = {selected_option}")
                
                # Find the question in the full question bank
                # Note: Since we randomized, we need to find by question text or use a different approach
                # For now, we'll use the question_id as it should match the renumbered questions
                question = next((q for q in all_questions if q.get('id') == question_id), None)
                if question:
                    is_correct = selected_option == question['correct_option']
                    if is_correct:
                        correct_answers += 1
                    
                    results.append({
                        "question_id": question_id,
                        "question_text": question['question_text'],
                        "selected_option": selected_option,
                        "correct_option": question['correct_option'],
                        "is_correct": is_correct,
                        "explanation": question.get('explanation', 'No explanation available')
                    })
                else:
                    print(f"⚠️ Question {question_id} not found")
            except Exception as e:
                print(f"⚠️ Error processing answer {answer}: {e}")
                continue
        
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        result_data = {
            "score": correct_answers,
            "total_questions": total_questions,
            "percentage": round(score_percentage, 1),
            "correct_answers": correct_answers,
            "wrong_answers": total_questions - correct_answers,
            "results": results,
            "quiz_type": "randomized",
            "subject": "maths",
            "total_questions_in_bank": len(all_questions)
        }
        
        print(f"✅ Randomized quiz submit successful: {correct_answers}/{total_questions} correct ({score_percentage:.1f}%)")
        return Response(result_data)
    
    except Exception as e:
        print(f"❌ Submit randomized quiz error: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return Response({
            "error": f"Failed to submit randomized quiz answers: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
