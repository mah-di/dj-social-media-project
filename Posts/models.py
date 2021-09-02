from django.db import models
from django.contrib.auth.models import User
from Profile.models import Notification
from .tasks import comment_notify, post_like_notify, comment_like_notify

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
        response = super().save(*args, **kwargs)
        
        if self.post.author != self.liker:
            post_like_notify.delay(self.post.author.pk, self.liker.pk, self.post.pk, self.pk)

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
        response = super().save(*args, **kwargs)

        if self.post.author != self.commentor:
            comment_notify.delay(self.post.author.pk, self.commentor.pk, self.post.pk, self.pk)

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
        response = super().save(*args, **kwargs)
        
        if self.comment.commentor != self.liker:
            comment_like_notify.delay(self.comment.commentor.pk, self.liker.pk, self.comment.post.pk, self.comment.pk, self.pk)
        
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