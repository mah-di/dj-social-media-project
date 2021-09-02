from celery import shared_task
from Profile.models import Notification
from . import models
from django.contrib.auth.models import User



@shared_task
def post_like_notify(user_pk, notifier_pk, post_obj_pk, like_obj_pk):
    user = User.objects.get(pk=user_pk)
    notifier = User.objects.get(pk=notifier_pk)
    post_obj = models.Post.objects.get(pk=post_obj_pk)
    like_obj = models.PostLike.objects.get(pk=like_obj_pk)

    Notification.objects.filter(user=user, post=post_obj, post_like=True).delete()

    likes = models.PostLike.objects.filter(post=post_obj).count()
    count = ''
    
    if likes == 2:
        count = f'and {likes-1} other'
    elif likes > 2:
        count = f'and {likes-1} others'

    Notification.objects.create(user=user, notifier=notifier, notification=f'{count} liked your post', post=post_obj, post_like=True, object=like_obj)

    return None




@shared_task
def comment_notify(user_pk, notifier_pk, post_obj_pk, comment_obj_pk):
    user = User.objects.get(pk=user_pk)
    notifier = User.objects.get(pk=notifier_pk)
    post_obj = models.Post.objects.get(pk=post_obj_pk)
    comment_obj = models.Comment.objects.get(pk=comment_obj_pk)

    Notification.objects.filter(user=user, post=post_obj, comment=True).delete()
    comments = models.Comment.objects.filter(post=post_obj)
    commentors = []
    for comment in comments:
        if comment.commentor != user and comment.commentor not in commentors:
            commentors.append(comment.commentor)

    count = len(commentors)
    counted = ''
    if count == 2:
        counted = f'and {count-1} other '
    elif count > 2:
        counted = f'and {count-1} others '
    
    Notification.objects.create(user=user, notifier=notifier, notification=f'{counted}commented on your post', post=post_obj, comment=True, object=comment_obj)




@shared_task
def comment_like_notify(user_pk, notifier_pk, post_obj_pk, comment_obj_pk, like_obj_pk):
    user = User.objects.get(pk=user_pk)
    notifier = User.objects.get(pk=notifier_pk)
    post_obj = models.Post.objects.get(pk=post_obj_pk)
    comment_obj = models.Comment.objects.get(pk=comment_obj_pk)
    like_obj = models.CommentLike.objects.get(pk=like_obj_pk)

    Notification.objects.filter(user=user, post=post_obj, comment_like=True).delete()
    count = models.CommentLike.objects.filter(comment=comment_obj).count()
    counted = ''
    if count == 2:
        counted = f'and {count-1} other'
    elif count > 2:
        counted = f'and {count-1} others'

    Notification.objects.create(user=user, notifier=notifier, notification=f'{counted} liked your comment', post=post_obj, comment_like=True, object=like_obj)