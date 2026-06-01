from django.contrib import admin
from .models import UploadedResume, ResumeAnalysis, SuggestedRole, ChatHistory

admin.site.register(UploadedResume)
admin.site.register(ResumeAnalysis)
admin.site.register(SuggestedRole)
admin.site.register(ChatHistory)
