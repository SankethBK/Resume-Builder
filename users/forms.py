from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'resume']

choices = [
    ("1" , "I am a manager"),
    ("2" , "I am a job seeker")
]
class ManagerForm(forms.Form):
    jobchoices = forms.ChoiceField(choices = choices ,widget = forms.RadioSelect, label = "Who are you?")
    company = forms.CharField(max_length = 200 , required = False)