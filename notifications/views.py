from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        # Mark all as read
        notifs.update(is_read=True)
    
    return render(request, "notifications.html", {'notifications': notifs})

