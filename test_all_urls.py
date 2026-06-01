import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
django.setup()

client = Client(SERVER_NAME='localhost')

urls_to_test = [
    '/',
    '/login/',
    '/logout/',
    '/signup/',
    '/forgot-password/',
    '/profile/',
    '/editprofile/',
    '/createjob/',
    '/joblist/',
    '/savedjobs/',
    '/applicationlist/',
    '/dashboard/',
    '/candidatedashboard/',
    '/recruiterdashboard/',
    '/notifications/',
]

errors = False
for url in urls_to_test:
    try:
        response = client.get(url)
        print(f"{url:<25} - {response.status_code}")
        if response.status_code == 500:
            print(f"ERROR: 500 on {url}")
            errors = True
    except Exception as e:
        print(f"EXCEPTION on {url}: {e}")
        errors = True

if errors:
    print("FINISHED WITH ERRORS")
else:
    print("FINISHED WITHOUT 500 ERRORS")
