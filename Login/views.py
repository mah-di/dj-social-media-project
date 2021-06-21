from django.shortcuts import render, redirect
from .forms import SignUpForm, SetUpProfileForm
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
    if req.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/account/signup/' and req.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/account/profile-setup/':
        return redirect('profile:profile')
    
    form = SetUpProfileForm()
    set_profile = True
    if req.method == 'POST':
        form = SetUpProfileForm(req.POST, req.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = req.user
            profile.save()
            return redirect('profile:profile')

    return render(req, 'Accounts/signup.html', context={'form':form, 'set_profile':set_profile})

# class ProfileSetUp(LoginRequiredMixin, CreateView):
#     model = UserProfile
#     fields = ('pro_pic', 'dob', 'bio', 'country', 'phone_number', 'facebook_profile', 'insta_profile',)
#     template_name = 'Accounts/signup.html'
#     context_object_name = 'form'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['set_profile'] = True

#         return context

#     def dispatch(self, request, *args, **kwargs):
#         if self.request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/account/signup/' and self.request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/account/profile-setup/':
#             raise Http404

#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         profile = form.save(commit=False)
#         profile.user = self.request.user
#         profile.save()
#         return redirect('profile:profile')

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

    return redirect('account:signup')
