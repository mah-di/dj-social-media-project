from django import template
from Posts.models import PostLike, CommentLike
from Profile.models import Notification


register = template.Library()

@register.filter
def post_liker(post):
    likers = list(PostLike.objects.filter(post=post).values_list('liker', flat=True))

    return likers


@register.filter
def comment_liker(comment):
    likers = list(CommentLike.objects.filter(comment=comment).values_list('liker', flat=True))

    return likers


@register.filter
def unread_count(notifications):
    unread = notifications.filter(unread=True).count()
    return unread


@register.filter
def as_list(followings):
    following_list = list(followings.values_list('follower', flat=True))

    return following_list


@register.filter
def alert(inbox_alert):
    if inbox_alert.filter(alert=True):
        return True
    
    return False