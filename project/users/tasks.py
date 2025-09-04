from celery import shared_task
from django.contrib.auth.models import User
from .models import Notification

@shared_task
def send_notification(user_id, message):
    user = User.objects.get(id=user_id)
    Notification.objects.create(user=user, message=message)
