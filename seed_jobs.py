import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
django.setup()

from django.contrib.auth.models import User
from jobs.models import Job
from user.models import Profile

def seed_jobs():
    # Ensure there is at least one recruiter
    recruiter_user, created = User.objects.get_or_create(
        username='recruiter_john',
        defaults={'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'}
    )
    if created:
        recruiter_user.set_password('password123')
        recruiter_user.save()
    
    # Update profile role to recruiter (signal creates it by default as candidate)
    profile = recruiter_user.profile
    if profile.role != 'recruiter':
        profile.role = 'recruiter'
        profile.save()

    jobs_data = [
        {
            'title': 'Frontend Developer',
            'company_name': 'Tech Solutions Inc.',
            'location': 'Remote',
            'salary': '$80,000 - $100,000',
            'job_type': 'Remote',
            'skills_required': 'React, JavaScript, CSS, HTML',
            'description': 'We are looking for an experienced Frontend Developer to join our fully remote team and build modern user interfaces.'
        },
        {
            'title': 'Backend Python Engineer',
            'company_name': 'DataCorp',
            'location': 'New York, NY',
            'salary': '$110,000 - $130,000',
            'job_type': 'Full Time',
            'skills_required': 'Python, Django, PostgreSQL, Docker',
            'description': 'Join DataCorp to scale our backend systems using Django and Python. Strong database knowledge is a plus.'
        },
        {
            'title': 'Data Science Intern',
            'company_name': 'AI Innovations',
            'location': 'San Francisco, CA',
            'salary': '$30/hr',
            'job_type': 'Internship',
            'skills_required': 'Python, Pandas, Machine Learning',
            'description': 'Summer internship for students interested in AI and Machine Learning. Work closely with our senior data scientists.'
        }
    ]

    count = 0
    for data in jobs_data:
        job, created = Job.objects.get_or_create(
            title=data['title'],
            recruiter=recruiter_user,
            defaults=data
        )
        if created:
            count += 1

    print(f"Successfully added {count} new jobs to the database under recruiter '{recruiter_user.username}'.")

if __name__ == '__main__':
    seed_jobs()
