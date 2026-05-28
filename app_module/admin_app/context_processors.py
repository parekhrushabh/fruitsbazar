from . import models
from django.contrib.auth.models import User

def admin_context(request):
    if request.path.startswith('/admin_side/'): # Adjust based on your URL pattern
        notifications = models.Notification.objects.filter(is_read=False).order_by('-id')[:5]
        total_notifications = models.Notification.objects.filter(is_read=False).count()
        return {
            'notifications': notifications,
            'total_notifications': total_notifications,
        }
    return {}
