from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Job(models.Model):

    JOB_TYPES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    company_name = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=200
    )

    salary = models.CharField(
        max_length=50
    )

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPES
    )

    skills_required = models.TextField()

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"

