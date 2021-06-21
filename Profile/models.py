from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

    def save(self, *args, **kwargs):
        response = super().save(*args, **kwargs)
        notification = Notification(user=self.following, notifier=self.follower, notification='started following you', follow=True, object=self)
        notification.save()

        return response


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notifier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifier')
    notification = models.CharField(max_length=400)
    post = models.ForeignKey('Posts.Post', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)
    
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    object = GenericForeignKey('model', 'object_id')

    follow = models.BooleanField(default=False)
    post_like = models.BooleanField(default=False)
    comment = models.BooleanField(default=False)
    comment_like = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.notifier} {self.notification}.'

    class Meta:
        ordering = ('-date',)