# AI Backend (FastAPI)

This is the AI-powered backend service that handles:
- 🤖 AI Quiz Generation (Quick Practice & Mock Tests)
- 💬 AI Chatbot for Student Questions
- 📝 AI Study Plan Generation
- 📚 AI Notes Generation

## Technology Stack
- **FastAPI**: Modern, fast Python web framework
- **OpenRouter API**: AI model access (using Gemini 2.0 Flash)
- **Python 3.8+**

## Features

### 1. Quick Practice (AI Quiz Generation)
- **Endpoint**: `/quiz`
- Generates 10 MCQ questions dynamically
- Supports multiple languages (English, Hindi, Tamil, Telugu, Kannada, Malayalam)
- Adaptive difficulty levels (simple, medium, hard)
- Curriculum data for Classes 7-10 (Computers, English, Maths, Science, History, Civics, Geography, Economics)

### 2. Mock Tests (AI Mock Test Generation)
- **Endpoint**: `/mock_test`
- Generates 50 MCQ questions for comprehensive testing
- Subject-wise and chapter-wise questions
- Progressive difficulty based on previous attempts

### 3. AI Assistant
- **Chat Endpoint**: `/ai-assistant/chat` - Conversational AI tutor
- **Study Plan**: `/ai-assistant/generate-study-plan` - Personalized study schedules
- **Notes Generator**: `/ai-assistant/generate-notes` - Chapter summaries and key concepts

## Setup Instructions

### 1. Install Dependencies
```bash
cd AI_BACKEND
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 3. Run the Server
```bash
python app.py
```

Or using uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**

## API Endpoints

### Quick Practice Endpoints
- `GET /classes` - Get available classes (7th, 8th, 9th, 10th)
- `GET /chapters?class_name=7th` - Get subjects for a class
- `GET /subtopics?class_name=7th&subject=Mathematics` - Get topics for a subject
- `GET /quiz?subtopic=...&language=English&currentLevel=1` - Generate quiz

### Mock Test Endpoints
- `GET /mock_classes` - Get available classes
- `GET /mock_subjects?class_name=7th` - Get subjects
- `GET /mock_chapters?class_name=7th&subject=Maths` - Get chapters
- `GET /mock_test?class_name=7th&subject=Maths&chapter=...&language=English` - Generate mock test

### AI Assistant Endpoints
- `POST /ai-assistant/chat` - Chat with AI tutor
- `POST /ai-assistant/generate-study-plan` - Generate study plan
- `POST /ai-assistant/generate-notes` - Generate notes

## Architecture

This service is **stateless** and doesn't require a database. It:
1. Receives requests from the frontend
2. Constructs prompts with curriculum data
3. Calls OpenRouter API (Gemini 2.0 Flash model)
4. Processes and returns AI-generated content

## Why Separate from Django?

✅ **Lightweight**: No database overhead for AI features
✅ **Fast**: FastAPI is optimized for API performance
✅ **Scalable**: Can be deployed independently
✅ **Maintainable**: Clear separation of concerns

## Production Deployment

For production, consider:
- Using a process manager like **Supervisor** or **systemd**
- Running behind **Nginx** as reverse proxy
- Setting up proper **CORS** for your frontend domain
- Monitoring API usage and costs
- Implementing rate limiting

## Troubleshooting

**Issue**: `OPENROUTER_API_KEY not found`
- **Solution**: Make sure `.env` file exists and contains valid API key

**Issue**: API calls fail
- **Solution**: Check your OpenRouter API key is valid and has credits

**Issue**: CORS errors from frontend
- **Solution**: CORS is already configured for `*` (all origins). In production, restrict to your domain.

## Support

For issues or questions, check:
- OpenRouter Documentation: https://openrouter.ai/docs
- FastAPI Documentation: https://fastapi.tiangolo.com

