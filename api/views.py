from rest_framework import viewsets, permissions
from jobs.models import Job
from applicant.models import Application
from .serializers import JobSerializer, ApplicationSerializer

class IsRecruiterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.recruiter == request.user

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class IsCandidateOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'candidate'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.candidate == request.user

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-applied_at')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'recruiter':
            return Application.objects.filter(job__recruiter=user).order_by('-applied_at')
        return Application.objects.filter(candidate=user).order_by('-applied_at')

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class JobRawAPIView(APIView):
    """
    An explicit APIView that implements all HTTP methods (GET, POST, PUT, PATCH, DELETE)
    and directly handles raw JSON payload via request.data.
    """
    permission_classes = [IsRecruiterOrReadOnly]

    def get(self, request, pk=None):
        if pk:
            job = get_object_or_404(Job, pk=pk)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        jobs = Job.objects.all().order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # request.data contains the parsed raw JSON data sent in the body
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recruiter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        self.check_object_permissions(request, job)
        # 'data=request.data' reads the raw JSON body
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        self.check_object_permissions(request, job)
        # partial=True allows omitting fields in the raw JSON body
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        self.check_object_permissions(request, job)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApplicationRawAPIView(APIView):
    """
    An explicit APIView that implements all HTTP methods (GET, POST, PUT, PATCH, DELETE)
    and directly handles raw JSON payload via request.data for Applications.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            application = get_object_or_404(Application, pk=pk)
            # Permission check
            if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
                if application.job.recruiter != request.user:
                    return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                if application.candidate != request.user:
                    return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = ApplicationSerializer(application)
            return Response(serializer.data)
        
        user = request.user
        if hasattr(user, 'profile') and user.profile.role == 'recruiter':
            applications = Application.objects.filter(job__recruiter=user).order_by('-applied_at')
        else:
            applications = Application.objects.filter(candidate=user).order_by('-applied_at')
        
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(candidate=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
            if application.job.recruiter != request.user:
                return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if application.candidate != request.user:
                return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
            if application.job.recruiter != request.user:
                return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if application.candidate != request.user:
                return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
            if application.job.recruiter != request.user:
                return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if application.candidate != request.user:
                return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)

        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
