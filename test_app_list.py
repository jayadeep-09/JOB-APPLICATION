import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'job.settings'
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from applicant.models import Application

# Check database
u = User.objects.get(username='karthik')
print(f"User: {u.username}, id={u.id}")
apps = Application.objects.filter(candidate=u)
print(f"Applications for karthik: {apps.count()}")
for a in apps:
    print(f"  ID={a.id}, job={a.job.title}, status={a.status}")

# Simulate the view request
c = Client()
c.force_login(u)
response = c.get('/applicationlist/')
print(f"\nResponse status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    print(f"'No Applications Yet' in page: {'No Applications Yet' in content}")
    print(f"'Systems Analyst' in page: {'Systems Analyst' in content}")
    print(f"'job-card' in page: {'job-card' in content}")
    
    # Show a snippet around applications context
    if hasattr(response, 'context') and response.context:
        ctx_apps = response.context.get('applications')
        if ctx_apps is not None:
            print(f"\nContext 'applications' count: {ctx_apps.count()}")
            for a in ctx_apps:
                print(f"  {a}")
        else:
            print("\nContext 'applications' is None!")
    
    # Check template used
    if hasattr(response, 'templates'):
        print(f"\nTemplates used: {[t.name for t in response.templates]}")
else:
    print(f"Unexpected status code: {response.status_code}")
    content = response.content.decode('utf-8')
    print(content[:500])
