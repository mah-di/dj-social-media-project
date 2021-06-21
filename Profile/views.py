from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView
from Login.models import UserProfile, User
from .forms import UserUpdateForm, UserProfileUpdateForm
from django.urls import reverse
from .models import Follow, Notification
from Posts.models import CommentLike, Post, Comment, PostLike

# Create your views here.
        
@login_required
def profile(req):
    return render(req, 'Profile/profile.html', context={})

@login_required
def update_profile(req):
    form1 = UserUpdateForm(instance=req.user)
    form2 = UserProfileUpdateForm(instance=req.user.profile)
    if req.method == 'POST':
        form1 = UserUpdateForm(data=req.POST, instance=req.user)
        form2 = UserProfileUpdateForm(data=req.POST, instance=req.user.profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('profile:profile')

    return render(req, 'Profile/user_update.html', context={'test':'working','form1':form1,'form2':form2})

class UpdatePfp(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ('set_pro_pic',)
    template_name = 'Profile/pf_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['propic'] = True

        return context
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user.pk != self.request.user.pk:
            raise Http404
        return super(UpdatePfp, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile:profile')


@login_required
def change_pass(req):
    user = req.user
    form = PasswordChangeForm(user)

    if req.method == 'POST':
        form = PasswordChangeForm(user, data=req.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(req, user)
            return redirect('profile:profile')

    return render(req, 'Profile/pf_change.html', context={'form':form})


@login_required
def check_notification(req, pk):
    notification = Notification.objects.get(pk=pk)
    notification.unread = False
    notification.save()
    if notification.post:
        return redirect('post:single_post', pk=notification.post.pk)
    else:
        return redirect('profile:user_profile', pk=notification.notifier.pk)


class OtherUserProfile(DetailView):
    model = User
    template_name = 'Profile/profile.html'
    context_object_name = 'other_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other'] = True

        return context

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() == request.user:
            return redirect('profile:profile')

        return super().dispatch(request, *args, **kwargs)


@login_required
def follow(req, pk):
    following = User.objects.get(pk=pk)
    follower = req.user
    if Follow.objects.filter(follower=follower, following=following):
        raise Http404

    new_follow = Follow(follower=follower, following=following)
    new_follow.save()

    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@login_required
def unfollow(req, pk):
    following = User.objects.get(pk=pk)
    follower = req.user
    new_follow = Follow.objects.get(follower=follower, following=following)
    new_follow.delete()

    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


def follower_list(req, pk):
    current_user = User.objects.get(pk=pk)
    follow = Follow.objects.filter(follower=req.user).values_list('following', flat=True)
    
    return render(req, 'Profile/users_list.html', context={'current_user':current_user, 'followers':True, 'follow':follow})


def following_list(req, pk):
    current_user = User.objects.get(pk=pk)
    follow = Follow.objects.filter(follower=req.user).values_list('following', flat=True)
    
    return render(req, 'Profile/users_list.html', context={'current_user':current_user, 'following':True, 'follow':follow})


def post_likers(req, pk):
    post = Post.objects.get(pk=pk)
    likes = PostLike.objects.filter(post=post)
    follow = Follow.objects.filter(follower=req.user).values_list('following', flat=True)
    
    return render(req, 'Profile/users_list.html', context={'likes':likes, 'like_list':True, 'follow':follow})


def comment_likers(req, pk):
    comment = Comment.objects.get(pk=pk)
    likes = CommentLike.objects.filter(comment=comment)
    follow = Follow.objects.filter(follower=req.user).values_list('following', flat=True)

    return render(req, 'Profile/users_list.html', context={'likes':likes, 'like_list':True, 'follow':follow})