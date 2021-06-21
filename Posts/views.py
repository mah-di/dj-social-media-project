from django.contrib.auth.models import User
from django.db.models.expressions import F
from Profile.models import Follow
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Comment, CommentLike, Post, PostLike
from Messages.models import Message
from Messages.forms import Share

# Create your views here.

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('image', 'caption',)
    template_name = 'Posts/post.html'
    context_object_name = 'form'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        return redirect('profile:profile')


class ViewPost(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'Posts/single-post.html'

    def comments_liked(self):
        return CommentLike.objects.filter(liker=self.request.user).values_list('comment', flat=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_liked'] = self.comments_liked()

        return context


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('caption',)
    context_object_name = 'form'
    template_name = 'Posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.pk

        return context

    def form_valid(self, form):
        form.save()
        return redirect('post:single_post', pk=self.object.pk)


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'Posts/delete.html'
    
    def get_success_url(self):
        return reverse('profile:profile')


@login_required
def feed(req):
    search = req.GET.get('search', '')
    results = User.objects.filter(username__contains=search)

    interests = Follow.objects.filter(follower=req.user).values_list('following', flat=True)
    posts = Post.objects.filter(author__in=interests)
    likes = PostLike.objects.filter(liker=req.user).values_list('post', flat=True)

    return render(req, 'Posts/feed.html', context={'posts':posts, 'likes':likes, 'search':search, 'results':results, 'following':interests})


@login_required
def post_like(req, pk):
    post = Post.objects.get(pk=pk)
    liked = PostLike.objects.filter(liker=req.user, post=post)
    if liked:
        pass
    else:
        like = PostLike(liker=req.user, post=post)
        like.save()

    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@login_required
def post_unlike(req, pk):
    post = Post.objects.get(pk=pk)
    liked = PostLike.objects.filter(liker=req.user, post=post)
    if liked:
        liked.delete()
    else:
        pass

    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@login_required
def write_comment(req, pk):
    if req.method == 'POST':
        comment = req.POST.get('comment')
        commentor = req.user
        post = Post.objects.get(pk=pk)
        form = Comment(comment=comment, commentor=commentor, post=post)
        form.save()
    
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


class EditComment(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ('comment',)
    context_object_name = 'form'
    template_name = 'Posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = True
        context['cmt_pk'] = self.object.pk

        return context

    def get_success_url(self):
        return reverse('post:single_post' , kwargs={'pk':self.object.post.pk})


@login_required
def delete_comment(req, pk):
    comment = Comment.objects.get(pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post:single_post', pk=post_pk)


@login_required
def comment_like(req, pk):
    comment = Comment.objects.get(pk=pk)
    liked = CommentLike.objects.filter(liker=req.user, comment=comment)
    if liked:
        pass
    else:
        like = CommentLike(liker=req.user, comment=comment)
        like.save()

    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@login_required
def comment_unlike(req, pk):
    comment = Comment.objects.get(pk=pk)
    liked = CommentLike.objects.filter(liker=req.user, comment=comment)
    if liked:
        liked.delete()
    else:
        pass

    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@login_required
def share_list(req, pk):
    interests = Follow.objects.filter(follower=req.user).values_list('following', flat=True)
    following = []
    for i in interests:
        following.append(User.objects.get(pk=i))

    return render(req, 'Posts/share.html', context={'pk':pk, 'following':following})


@login_required
def share(req, pk):
    if req.method == 'POST':
        post_pk = req.POST.get('post')
        post = Post.objects.get(pk=post_pk)
        share = Message(attachment=post)
        share.sender = req.user
        share.receiver = User.objects.get(pk=pk)
        share.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])