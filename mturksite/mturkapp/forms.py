from .models import HIT, HITType, Qualification
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class qualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification 
        fields = ['nickname', 'qualID', 'comparator', 'int_value', 'country', 'subdivision', 'actions_guarded']


class hitForm(forms.ModelForm):
    hittype = forms.CharField(max_length=254)
    class Meta:
        model = HIT
        fields = ['max_assignments', 'expiry_time']
        
       
        

class hittypeForm(forms.ModelForm):
    class Meta:
        model = HITType
        fields = ['title','description', 'keyword', 'reward', 'quals']
