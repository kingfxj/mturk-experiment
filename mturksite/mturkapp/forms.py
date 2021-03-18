from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class qualificationForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, required=True)
    country = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Qualification 
        fields = ['nickname', 'description','comparator', 'int_value', 'subdivision']
       
class hitForm(forms.ModelForm):
    hittype = forms.CharField(max_length=254)
    class Meta:
        model = HIT
        fields = ['max_assignments', 'expiry_time']

class hittypeForm(forms.ModelForm):
    quals = forms.CharField(max_length=200)
    class Meta:
        model = HITType
        fields = ['title', 'description', 'keyword', 'reward']

class expForm(forms.ModelForm):
    class Meta:
        model = exp
        fields = ['title']
