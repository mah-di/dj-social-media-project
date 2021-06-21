from django import forms
from Login.models import User, UserProfile
from phonenumber_field.formfields import PhoneNumberField


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

class UserProfileUpdateForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=False)
    dob = forms.DateField(required=False, widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = UserProfile
        fields = ('bio', 'dob', 'country', 'phone_number', 'facebook_profile', 'insta_profile')