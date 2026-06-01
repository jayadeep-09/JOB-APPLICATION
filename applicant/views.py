import logging

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Application
from jobs.models import Job
from .forms import ApplicationForm
from notifications.models import Notification

logger = logging.getLogger(__name__)

@login_required
def application_list(request):
    # If recruiter, show applications for their jobs
    if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
        applications = Application.objects.select_related('candidate', 'job').filter(job__recruiter=request.user).order_by('-applied_at')
        
        # Handle status update
        if request.method == 'POST':
            app_id = request.POST.get('application_id')
            new_status = request.POST.get('status')
            if app_id and new_status in dict(Application.STATUS_CHOICES):
                application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
                application.status = new_status
                application.save()
                
                # Create Notification for candidate
                Notification.objects.create(
                    user=application.candidate,
                    title=f"Application Update: {application.job.title}",
                    message=f"Your application for {application.job.title} at {application.job.company_name} is now {new_status}."
                )
                messages.success(request, f"Application status updated to {new_status}.")
                return redirect('applicationlist')
                
    else:
        # Candidate sees their own applications
        applications = Application.objects.select_related('job').filter(candidate=request.user).order_by('-applied_at')
        
    return render(request, "application_list.html", {'applications': applications})

@login_required
def apply(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
        messages.error(request, "Recruiters cannot apply for jobs.")
        return redirect('home')

    job_id = request.GET.get('job_id') or request.POST.get('job_id')
    if not job_id:
        messages.error(request, "Please choose a job before applying.")
        return redirect('joblist')
    
    job = get_object_or_404(Job, id=job_id)
    job_details_url = f"{reverse('jobdetails')}?id={job.id}"
    
    # Check if already applied
    if Application.objects.filter(candidate=request.user, job=job).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect(job_details_url)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    if Application.objects.select_for_update().filter(candidate=request.user, job=job).exists():
                        messages.info(request, "You have already applied for this job.")
                        return redirect(job_details_url)

                    application = form.save(commit=False)
                    application.candidate = request.user
                    application.job = job
                    application.save()
            except Exception:
                logger.exception("Failed to save application for user_id=%s job_id=%s", request.user.id, job.id)
                messages.error(request, "We could not submit your application. Please try again.")
                return render(request, "jobs/apply_job.html", {'form': form, 'job': job})
            
            # Notify recruiter
            try:
                Notification.objects.create(
                    user=job.recruiter,
                    title=f"New Application for {job.title}",
                    message=f"{request.user.username} has applied for {job.title}."
                )
            except Exception:
                logger.exception("Application notification failed for application_id=%s", application.id)
            
            messages.success(request, f"Successfully applied to {job.title}!")
            return redirect(job_details_url)
        messages.error(request, "Please correct the errors below before submitting.")
    else:
        form = ApplicationForm()
        
    return render(request, "jobs/apply_job.html", {'form': form, 'job': job})
