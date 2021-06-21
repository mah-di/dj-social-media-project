from django.db import models
from django.contrib.auth.models import User
from Profile.models import Notification

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=2000, verbose_name='Write a Captioin', blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-post_date',)

class PostLike(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_liked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liker} likes {self.post}'

    def save(self, *args, **kwargs):
        Notification.objects.filter(user=self.post.author, post=self.post, post_like=True).delete()
        count = PostLike.objects.filter(post=self.post).count()
        counted = ''
        if count == 1:
            counted = f'and {count} other '
        elif count > 1:
            counted = f'and {count} others '

        response = super().save(*args, **kwargs)
        
        if self.post.author != self.liker:
            notification = Notification(user=self.post.author, notifier=self.liker, notification=f'{counted}liked your post', post=self.post, post_like=True, object=self)
            notification.save()

        return response
    
    class Meta:
        ordering = ('-like_date',)

class Comment(models.Model):
    comment = models.TextField(verbose_name='Write a comment..', max_length=1000, default='')
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.commentor} commented on {self.post}'

    def save(self, *args, **kwargs):
        Notification.objects.filter(user=self.post.author, post=self.post, comment=True).delete()
        comments = Comment.objects.filter(post=self.post)
        commentors = []
        for comment in comments:
            if comment.commentor != self.post.author and comment.commentor not in commentors:
                commentors.append(comment.commentor)

        count = len(commentors)
        counted = ''
        if count == 1:
            counted = f'and {count} other '
        elif count > 1:
            counted = f'and {count} others '

        response = super().save(*args, **kwargs)

        if self.post.author != self.commentor:
            notification = Notification(user=self.post.author, notifier=self.commentor, notification=f'{counted}commented on your post', post=self.post, comment=True, object=self)
            notification.save()

        return response
    
    class Meta:
        ordering = ('-comment_date',)

class CommentLike(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_liked')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liker} likes {self.comment}'

    def save(self, *args, **kwargs):
        Notification.objects.filter(user=self.comment.commentor, post=self.comment.post, comment_like=True).delete()
        count = CommentLike.objects.filter(comment=self.comment).count()
        counted = ''
        if count == 1:
            counted = f'and {count} other '
        elif count > 1:
            counted = f'and {count} others '

        response = super().save(*args, **kwargs)
        
        if self.comment.commentor != self.liker:
            notification = Notification(user=self.comment.commentor, notifier=self.liker, notification=f'{counted}liked your comment', post=self.comment.post, comment_like=True, object=self)
            notification.save()
        
        return response
    
    class Meta:
        ordering = ('-like_date',)

class Share(models.Model):
    sharer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared')
    caption = models.CharField(max_length=400, blank=True)
    share_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sharer} shared {self.post}'
    
    class Meta:
        ordering = ('-share_date',)