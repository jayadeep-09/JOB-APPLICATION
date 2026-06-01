import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, Client
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
django.setup()

from chatbot.models import UploadedResume, ResumeAnalysis, SuggestedRole, ChatHistory
from chatbot.views import upload_resume, chat_message

def run_tests():
    print("Testing Chatbot integration...")
    factory = RequestFactory()
    
    # 1. Test Chatbot Upload API with mock PDF
    # Create a mock PDF content (usually PDF requires actual bytes but we'll try a dummy string or rely on the parser fallback)
    # The pdfplumber parser might fail on dummy strings, but our ai_engine handles empty gracefully or we can just test if the endpoint is reachable.
    print("Creating mock request...")
    mock_pdf = SimpleUploadedFile("test_resume.pdf", b"%PDF-1.4 mock content", content_type="application/pdf")
    request = factory.post('/chatbot/api/upload/', {'resume': mock_pdf})
    request.session = factory.get('/').session
    if not hasattr(request, 'session'):
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
    
    response = upload_resume(request)
    print(f"Upload Response Status: {response.status_code}")
    
    # 2. Test Chat Message API
    chat_req = factory.post('/chatbot/api/chat/', {'message': 'What is my score?'})
    chat_req.session = request.session
    chat_req.session.save()
    
    chat_resp = chat_message(chat_req)
    print(f"Chat Response Status: {chat_resp.status_code}")
    
    if chat_resp.status_code == 200:
        data = json.loads(chat_resp.content.decode())
        print(f"Chat Reply: {data.get('reply')}")
        
    print("Tests completed.")

if __name__ == '__main__':
    run_tests()
