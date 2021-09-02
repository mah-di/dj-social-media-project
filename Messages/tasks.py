from celery import shared_task
from . import models
from django.contrib.auth.models import User



@shared_task
def message_alert(sender_pk, receiver_pk, preview_text):
    sender = User.objects.get(pk=sender_pk)
    receiver = User.objects.get(pk=receiver_pk)

    check = models.InboxAlert.objects.filter(sender=sender, receiver=receiver)
    if not check:
        models.InboxAlert(sender=sender, receiver=receiver).save()
        models.InboxAlert(sender=receiver, receiver=sender, alert=False).save()
    models.InboxAlert.objects.filter(sender=sender, receiver=receiver).update(alert=True)
    update = models.InboxAlert.objects.get(sender=sender, receiver=receiver)
    update.message = preview_text
    update.save()
    update = models.InboxAlert.objects.get(sender=receiver, receiver=sender)
    update.message = 'You : ' + preview_text
    update.save()

    return None