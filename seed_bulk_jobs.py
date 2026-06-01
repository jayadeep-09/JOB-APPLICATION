import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
django.setup()

from django.contrib.auth.models import User
from jobs.models import Job

def seed_bulk_jobs():
    recruiter_user, _ = User.objects.get_or_create(
        username='recruiter_john',
        defaults={'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'}
    )
    profile = recruiter_user.profile
    if profile.role != 'recruiter':
        profile.role = 'recruiter'
        profile.save()

    job_titles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer', 'DevOps Engineer', 'QA Tester', 'Frontend Developer', 'Backend Developer', 'Machine Learning Engineer', 'Systems Analyst']
    companies = ['TechNova', 'DataSphere', 'CloudNet', 'InnovateAI', 'CyberShield', 'NextGen Solutions', 'Quantum Leap', 'BlueOcean Tech', 'Pioneer Systems', 'Apex Dynamics']
    locations = ['San Francisco, CA', 'New York, NY', 'Austin, TX', 'Remote', 'Seattle, WA', 'London, UK', 'Berlin, Germany', 'Toronto, ON', 'Sydney, AU', 'Remote']
    types = ['Full Time', 'Part Time', 'Internship', 'Remote']
    salaries = ['$60,000 - $80,000', '$90,000 - $120,000', '$130,000 - $160,000', '$150,000+', '$40/hr', 'Competitive']
    skills = ['Python, Django', 'React, Node.js', 'Java, Spring Boot', 'AWS, Docker, Kubernetes', 'Figma, Sketch', 'SQL, Pandas, Scikit-learn', 'C++, Unreal Engine', 'Ruby on Rails', 'Go, Microservices', 'Cybersecurity, Networking']

    count = 0
    for i in range(20):
        title = random.choice(job_titles)
        company = random.choice(companies)
        location = random.choice(locations)
        job_type = random.choice(types)
        salary = random.choice(salaries)
        skill = random.choice(skills)
        
        # If job type is remote, set location to remote sometimes
        if job_type == 'Remote':
            location = 'Remote'

        job = Job.objects.create(
            recruiter=recruiter_user,
            title=f"{title} - Level {random.randint(1, 5)}",
            company_name=company,
            location=location,
            salary=salary,
            job_type=job_type,
            skills_required=skill,
            description=f"We are looking for a talented {title} to join our team at {company}. You will be responsible for driving key initiatives and working closely with cross-functional teams."
        )
        count += 1

    print(f"Successfully added {count} new bulk jobs.")

if __name__ == '__main__':
    seed_bulk_jobs()
