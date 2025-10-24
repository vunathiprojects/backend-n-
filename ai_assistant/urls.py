from django.urls import path
from . import views

urlpatterns = [
    # Save AI content endpoints
    path('save-study-plan/', views.save_ai_study_plan, name='save_ai_study_plan'),
    path('save-ai-note/', views.save_ai_generated_note, name='save_ai_generated_note'),
    path('save-manual-note/', views.save_manual_note, name='save_manual_note'),
    path('save-chat-message/', views.save_chat_message, name='save_chat_message'),
    
    # Get content endpoints
    path('study-plans/', views.get_study_plans, name='get_study_plans'),
    path('ai-notes/', views.get_ai_notes, name='get_ai_notes'),
    path('manual-notes/', views.get_manual_notes, name='get_manual_notes'),
    path('chat-history/', views.get_chat_history, name='get_chat_history'),
    path('all-notes/', views.get_all_notes, name='get_all_notes'),
    
    # Update/Delete endpoints
    path('manual-notes/<int:note_id>/', views.update_manual_note, name='update_manual_note'),
    path('manual-notes/<int:note_id>/delete/', views.delete_manual_note, name='delete_manual_note'),
    
    # Favorites endpoints
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.get_favorites, name='get_favorites'),
]
