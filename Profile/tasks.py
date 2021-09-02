from celery import shared_task
from . import models
from django.contrib.auth.models import User


@shared_task
def new_follow_notify(user_pk, notifier_pk, follow_obj_pk):
    user = User.objects.get(pk=user_pk)
    notifier = User.objects.get(pk=notifier_pk)
    follow_obj = models.Follow.objects.get(pk=follow_obj_pk)
    
    models.Notification.objects.create(user=user, notifier=notifier, notification='started following you', follow=True, object=follow_obj)

    return None