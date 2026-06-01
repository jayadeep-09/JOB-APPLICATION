from django.db import models
from django.contrib.auth.models import User
import uuid

class UploadedResume(models.Model):
    # Optional candidate link, can also be used by anonymous users via session_id
    candidate = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to='chatbot_resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} uploaded at {self.uploaded_at}"

class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(UploadedResume, on_delete=models.CASCADE, related_name='analysis')
    extracted_text = models.TextField()
    skills = models.JSONField(default=list)
    experience = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    technologies = models.JSONField(default=list)
    ats_score = models.IntegerField(default=0)
    improvements = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Analysis for {self.resume.id}"

class SuggestedRole(models.Model):
    analysis = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='suggested_roles')
    role_title = models.CharField(max_length=150)
    match_percentage = models.IntegerField()
    missing_skills = models.JSONField(default=list)

    def __str__(self):
        return f"{self.role_title} ({self.match_percentage}%)"

class ChatHistory(models.Model):
    # Link chat history to either user or session
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    resume = models.ForeignKey(UploadedResume, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message[:20]}"
