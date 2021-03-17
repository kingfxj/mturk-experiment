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

# class qualificationForm(forms.Form):
#     nickname = forms.CharField(max_length=100)
#     description = forms.CharField(max_length=2000)
#     comparator = forms.CharField(max_length=50)
#     int_value = forms.IntegerField(required=False)
#     country = forms.CharField(max_length=100, required=False)
#     subdivision = forms.CharField(max_length=100, required=False)
        
class hitForm(forms.ModelForm):
    class Meta:
        model = HIT
        fields = ['hit_id', 'hittype_id', 'assignments', 'expiry_date']

class hittypeForm(forms.ModelForm):
    class Meta:
        model = HITType
        fields = ['batch', 'title', 'hittype_id', 'description', 'keyword', 'reward', 'quals']
