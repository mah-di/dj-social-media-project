from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder':'Your First Name', 'style':'margin-bottom: 20px'}))
    last_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder':'Your Last Name', 'style':'margin-bottom: 20px'}))
    username = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder':'UserName', 'style':'margin-bottom: 20px'}))
    email = forms.EmailField(required=True, label='', widget=forms.TextInput(attrs={'placeholder':'Email', 'style':'margin-bottom: 20px'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class SetUpProfileForm(forms.ModelForm):
    dob = forms.DateField(required=False, widget=forms.TextInput(attrs={'type':'date'}))
    bio = forms.Textarea()
    class Meta:
        model = UserProfile
        fields = ('set_pro_pic', 'dob', 'bio', 'country', 'phone_number', 'facebook_profile', 'insta_profile')