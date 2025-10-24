# Generated manually for AI Assistant models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AIStudyPlan',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('chapter', models.CharField(max_length=200)),
                ('subtopic', models.CharField(blank=True, max_length=200, null=True)),
                ('plan_title', models.CharField(max_length=200)),
                ('plan_content', models.TextField()),
                ('plan_type', models.CharField(default='study_plan', max_length=50)),
                ('difficulty_level', models.CharField(default='medium', max_length=20)),
                ('estimated_duration_hours', models.IntegerField(default=1)),
                ('is_favorite', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AI Study Plan',
                'verbose_name_plural': 'AI Study Plans',
                'db_table': 'ai_study_plans',
            },
        ),
        migrations.CreateModel(
            name='AIGeneratedNote',
            fields=[
                ('note_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('chapter', models.CharField(max_length=200)),
                ('subtopic', models.CharField(blank=True, max_length=200, null=True)),
                ('note_title', models.CharField(max_length=200)),
                ('note_content', models.TextField()),
                ('note_type', models.CharField(default='ai_generated', max_length=50)),
                ('key_points', models.TextField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('is_favorite', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AI Generated Note',
                'verbose_name_plural': 'AI Generated Notes',
                'db_table': 'ai_generated_notes',
            },
        ),
        migrations.CreateModel(
            name='ManualNote',
            fields=[
                ('note_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('chapter', models.CharField(max_length=200)),
                ('subtopic', models.CharField(blank=True, max_length=200, null=True)),
                ('note_title', models.CharField(blank=True, max_length=200, null=True)),
                ('note_content', models.TextField()),
                ('note_type', models.CharField(default='manual', max_length=50)),
                ('color', models.CharField(default='#fef3c7', max_length=7)),
                ('is_important', models.BooleanField(default=False)),
                ('tags', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Manual Note',
                'verbose_name_plural': 'Manual Notes',
                'db_table': 'manual_notes',
            },
        ),
        migrations.CreateModel(
            name='AIChatHistory',
            fields=[
                ('chat_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('chapter', models.CharField(max_length=200)),
                ('subtopic', models.CharField(blank=True, max_length=200, null=True)),
                ('user_message', models.TextField()),
                ('ai_response', models.TextField()),
                ('response_type', models.CharField(default='general', max_length=50)),
                ('message_timestamp', models.DateTimeField(auto_now_add=True)),
                ('session_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_favorite', models.BooleanField(default=False)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AI Chat History',
                'verbose_name_plural': 'AI Chat History',
                'db_table': 'ai_chat_history',
            },
        ),
        migrations.CreateModel(
            name='AIInteractionSession',
            fields=[
                ('session_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('chapter', models.CharField(max_length=200)),
                ('subtopic', models.CharField(blank=True, max_length=200, null=True)),
                ('session_type', models.CharField(default='general', max_length=50)),
                ('total_messages', models.IntegerField(default=0)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AI Interaction Session',
                'verbose_name_plural': 'AI Interaction Sessions',
                'db_table': 'ai_interaction_sessions',
            },
        ),
        migrations.CreateModel(
            name='AIFavorite',
            fields=[
                ('favorite_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_type', models.CharField(max_length=50)),
                ('content_id', models.IntegerField()),
                ('favorite_title', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AI Favorite',
                'verbose_name_plural': 'AI Favorites',
                'db_table': 'ai_favorites',
            },
        ),
    ]