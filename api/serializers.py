from rest_framework import serializers
from django.contrib.auth.models import User
from jobs.models import Job
from applicant.models import Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']

class JobSerializer(serializers.ModelSerializer):
    recruiter = UserSerializer(read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['candidate', 'applied_at']
