from django.shortcuts import render, redirect
from .forms import SignUpForm, SetUpProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def signup(req):
    if req.user.is_authenticated:
        return redirect('profile:profile')

    form = SignUpForm()
    success = False

    if req.method == 'POST':
        form = SignUpForm(data=req.POST)
        if form.is_valid():
            form.save()
            success = True
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(req, user)
                return redirect('account:setup_profile')

    return render(req, 'Accounts/signup.html', context={'form':form, 'success':success})

@login_required
def setup_profile(req):
    profile = UserProfile.objects.get_or_create(user=req.user)[0]
    form = SetUpProfileForm(instance=profile)
    
    if req.method == 'POST':
        form = SetUpProfileForm(req.POST, req.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile:profile')

    return render(req, 'Accounts/signup.html', context={'form':form, 'set_profile':True})

def user_login(req):
    if req.user.is_authenticated:
        return redirect('profile:profile')

    form = AuthenticationForm()
    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('post:feed')

    return render(req, 'Accounts/signup.html', context={'form':form, 'login':True})

@login_required
def user_logout(req):
    logout(req)

    return redirect('account:login')
