from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

from .forms import SignupForm, ProfileUpdateForm
from .models import Profile
from jobs.models import Job

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Find the user by email since the form uses email
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
        except User.MultipleObjectsReturned:
            user_obj = User.objects.filter(email=email).first()
            username = user_obj.username

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, "accounts/login.html")

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            phone = form.cleaned_data.get('phone')
            profile = user.profile
            profile.role = role
            if phone:
                profile.phone = phone
            profile.save()
            messages.success(request, "Account created successfully! You can now login.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignupForm()

    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, "accounts/profile.html", {'user': request.user})

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "accounts/profile.html", {'form': form, 'edit_mode': True})

def home(request):
    jobs = Job.objects.all().order_by('-created_at')[:6]
    applied_job_ids = []
    if request.user.is_authenticated:
        from applicant.models import Application
        applied_job_ids = list(Application.objects.filter(candidate=request.user).values_list('job_id', flat=True))
    return render(request, "home.html", {'jobs': jobs, 'applied_job_ids': applied_job_ids})

