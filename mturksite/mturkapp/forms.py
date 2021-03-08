from .models import Assignment, Qualification
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class assignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'surname', 'birthYear', 'birthCity', 'active']

class qualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification 
        fields = ['nickname', 'qualID', 'comparator', 'int_value', 'country', 'subdivision', 'actions_guarded']