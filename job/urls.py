from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from applicant import views as test_view
from user import views
from jobs import views as job_view
from dashboard import views as das
from notifications import views as noti

urlpatterns = [

    path('admin/', admin.site.urls),

    # HOME
    path('', views.home, name='home'),

    # USER
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='accounts/forgot_password.html', email_template_name='accounts/password_reset_email.html', success_url='/password_reset_done/'), name='forgotpassword'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', success_url='/password_reset_complete/'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),

    # JOBS
    path('createjob/', job_view.create, name='createjob'),
    path('editjob/<int:job_id>/', job_view.edit_job, name='editjob'),
    path('deletejob/<int:job_id>/', job_view.delete_job, name='deletejob'),
    path('jobdetails/', job_view.details, name='jobdetails'),
    path('joblist/', job_view.job_list, name='joblist'),
    path('savedjobs/', job_view.saved, name='savedjobs'),
    path('toggle_save/', job_view.toggle_save, name='toggle_save'),

    # APPLICATIONS
    path('applyjob/', test_view.apply, name='applyjob'),
    path('applicationlist/', test_view.application_list, name='applicationlist'),

    # DASHBOARD
    path('dashboard/', das.recruiter, name='dashboard'),
    path('candidatedashboard/', das.candidate, name='candidatedashboard'),
    path('recruiterdashboard/', das.recruiter, name='recruiterdashboard'),

    # NOTIFICATIONS
    path('notifications/', noti.notifications, name='notifications'),

    # API
    path('api/', include('api.urls')),

    # CHATBOT
    path('chatbot/', include('chatbot.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
