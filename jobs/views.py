from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, SavedJob
from .forms import JobCreationForm

@login_required
def create(request):
    if hasattr(request.user, 'profile') and request.user.profile.role != 'recruiter':
        messages.error(request, "Only recruiters can post jobs.")
        return redirect('home')

    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job created successfully!")
            return redirect('jobdetails') # Update with id later if needed, but the original path didn't have id
    else:
        form = JobCreationForm()
    return render(request, "create_job.html", {'form': form})

@login_required
def details(request):
    job_id = request.GET.get('id')
    if not job_id:
        return redirect('joblist')
    job = get_object_or_404(Job, id=job_id)
    
    is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    
    from applicant.models import Application
    is_applied = False
    applied_job_ids = []
    if request.user.is_authenticated:
        is_applied = Application.objects.filter(candidate=request.user, job=job).exists()
        applied_job_ids = list(Application.objects.filter(candidate=request.user).values_list('job_id', flat=True))
        
    similar_jobs = Job.objects.filter(job_type=job.job_type).exclude(id=job.id).order_by('-created_at')[:3]
    
    return render(request, "jobs/job_detail.html", {
        'job': job, 
        'is_saved': is_saved, 
        'is_applied': is_applied,
        'similar_jobs': similar_jobs,
        'applied_job_ids': applied_job_ids
    })

def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    
    q = request.GET.get('q')
    location = request.GET.get('location')
    category = request.GET.get('category')
    job_type = request.GET.get('type')
    salary = request.GET.get('salary')

    if q:
        jobs = jobs.filter(title__icontains=q) | jobs.filter(company_name__icontains=q)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__iexact=category)
    if job_type:
        jobs = jobs.filter(job_type__iexact=job_type)
    if salary:
        jobs = jobs.filter(salary__gte=int(salary))
        
    applied_job_ids = []
    if request.user.is_authenticated:
        from applicant.models import Application
        applied_job_ids = [app_id for app_id in Application.objects.filter(candidate=request.user).values_list('job_id', flat=True)]
        
    return render(request, "jobs/jobs_list.html", {'jobs': jobs, 'applied_job_ids': applied_job_ids})

@login_required
def saved(request):
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, "jobs/saved_jobs.html", {'saved_jobs': saved_jobs})

@login_required
def toggle_save(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        if not created:
            saved_job.delete()
            messages.success(request, "Job removed from saved list.")
        else:
            messages.success(request, "Job saved successfully!")
        
        # Redirect back to where they came from
        next_url = request.POST.get('next', 'joblist')
        return redirect(next_url)
    return redirect('joblist')

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == 'POST':
        form = JobCreationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('recruiterdashboard')
    else:
        form = JobCreationForm(instance=job)
    return render(request, 'create_job.html', {'form': form, 'edit_mode': True})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
    return redirect('recruiterdashboard')

