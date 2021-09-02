from django.db import models
from django.contrib.auth.models import User
from Posts.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import message_alert

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    message = models.CharField(verbose_name='Type your message..', max_length=2000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    attachment = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    picture = models.ImageField(upload_to='message', blank=True)
    preview = models.CharField(max_length=100, default='')

    def save(self, *args, **kwargs):
        if self.message != '':
            self.preview = self.message[:50]
        elif self.attachment is not None:
            self.preview = f'sent an attachment.'
        else:
            self.preview = f'sent a media.'

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('date',)


class InboxAlert(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_from')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_to')
    alert = models.BooleanField(default=True)
    last_alert = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ('-last_alert',)


@receiver(post_save, sender=Message)
def msg_alert(sender, instance, **kwargs):
    message_alert.delay(instance.sender.pk, instance.receiver.pk, instance.preview)