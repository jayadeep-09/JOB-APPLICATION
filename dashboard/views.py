from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job, SavedJob
from applicant.models import Application

@login_required
def candidate(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
        return redirect('recruiterdashboard')
        
    jobs_applied = Application.objects.filter(candidate=request.user).count()
    saved_jobs = SavedJob.objects.filter(user=request.user).count()
    pending_applications = Application.objects.filter(candidate=request.user, status='Pending').count()
    
    context = {
        'jobs_applied': jobs_applied,
        'saved_jobs': saved_jobs,
        'pending_applications': pending_applications
    }
    return render(request, "candidate_dashboard.html", context)

@login_required
def recruiter(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'candidate':
        return redirect('candidatedashboard')
        
    active_jobs = Job.objects.filter(recruiter=request.user).count()
    total_applications = Application.objects.filter(job__recruiter=request.user).count()
    pending_applications = Application.objects.filter(job__recruiter=request.user, status='Pending').count()
    
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    applications = Application.objects.select_related('candidate', 'job').filter(job__recruiter=request.user).order_by('-applied_at')
    
    context = {
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'jobs': jobs,
        'applications': applications
    }
    return render(request, "jobs/recruiter_dashboard.html", context)
