import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedResume, ResumeAnalysis, SuggestedRole, ChatHistory
from .services.resume_parser import parse_resume
from .services.ai_engine import extract_entities, suggest_roles, calculate_ats_score, generate_chat_response

def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST':
        if 'resume' not in request.FILES:
            return JsonResponse({'error': 'No resume file provided'}, status=400)
            
        file_obj = request.FILES['resume']
        filename = file_obj.name
        
        if not (filename.lower().endswith('.pdf') or filename.lower().endswith('.docx')):
            return JsonResponse({'error': 'Invalid file format. Only PDF and DOCX are supported.'}, status=400)
            
        session_id = get_session_id(request)
        user = request.user if request.user.is_authenticated else None
        
        # Save resume
        resume = UploadedResume.objects.create(
            candidate=user,
            session_id=session_id,
            file=file_obj
        )
        
        # Parse text
        text = parse_resume(file_obj, filename)
        
        if not text.strip():
            return JsonResponse({'error': 'Could not extract text from the file.'}, status=400)
            
        # Analyze with AI
        entities = extract_entities(text)
        ats_score, improvements = calculate_ats_score(text, entities['skills'])
        
        analysis = ResumeAnalysis.objects.create(
            resume=resume,
            extracted_text=text,
            skills=entities['skills'],
            technologies=entities['technologies'],
            experience=entities['experience'],
            education=entities['education'],
            ats_score=ats_score,
            improvements=improvements
        )
        
        # Suggestions
        suggestions = suggest_roles(text, entities['skills'])
        for sug in suggestions:
            SuggestedRole.objects.create(
                analysis=analysis,
                role_title=sug['role_title'],
                match_percentage=sug['match_percentage'],
                missing_skills=sug['missing_skills']
            )
            
        # Save system message
        ChatHistory.objects.create(
            user=user,
            session_id=session_id,
            resume=resume,
            message="I've successfully analyzed your resume. I found your skills and generated some job suggestions. What would you like to know?",
            is_bot=True
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Resume analyzed successfully',
            'analysis': {
                'skills': analysis.skills,
                'ats_score': analysis.ats_score,
                'suggestions': suggestions
            }
        })
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def chat_message(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)
            
        session_id = get_session_id(request)
        user = request.user if request.user.is_authenticated else None
        
        # Find latest uploaded resume for context
        resume = None
        if user:
            resume = UploadedResume.objects.filter(candidate=user).order_by('-uploaded_at').first()
        if not resume and session_id:
            resume = UploadedResume.objects.filter(session_id=session_id).order_by('-uploaded_at').first()
            
        # Save user message
        ChatHistory.objects.create(
            user=user,
            session_id=session_id,
            resume=resume,
            message=message,
            is_bot=False
        )
        
        analysis = None
        suggestions = []
        if resume and hasattr(resume, 'analysis'):
            analysis = resume.analysis
            suggestions = list(analysis.suggested_roles.all())
            
        # Generate AI response
        bot_reply = generate_chat_response(message, analysis, suggestions)
        
        ChatHistory.objects.create(
            user=user,
            session_id=session_id,
            resume=resume,
            message=bot_reply,
            is_bot=True
        )
        
        return JsonResponse({
            'success': True,
            'reply': bot_reply
        })
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_history(request):
    session_id = get_session_id(request)
    user = request.user if request.user.is_authenticated else None
    
    if user:
        history = ChatHistory.objects.filter(user=user).order_by('timestamp')
    else:
        history = ChatHistory.objects.filter(session_id=session_id).order_by('timestamp')
        
    data = []
    for h in history:
        data.append({
            'is_bot': h.is_bot,
            'message': h.message,
            'timestamp': h.timestamp.isoformat()
        })
        
    return JsonResponse({'history': data[-50:]}) # Return last 50 messages
