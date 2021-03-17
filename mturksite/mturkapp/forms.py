from .models import HIT, HITType, Qualification
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class qualificationForm(forms.ModelForm):  # deprecated code
#     # comparator = forms.ChoiceField(max_length=50, widget=forms.Select(choices=comparator_choices),)
#     # comparator = forms.ModelChoiceField(queryset = Qualification.objects.all(), initial=0)
#     class Meta:
#         model = Qualification 
#         # fields = ['nickname', 'qualID', 'comparator', 'int_value', 'country', 'subdivision', 'actions_guarded']
#         fields = ['nickname', 'comparator', 'int_value', 'country', 'subdivision', 'actions_guarded']

class qualificationForm(forms.Form):
    nickname = forms.CharField(max_length=100)
    description = forms.CharField(max_length=2000)
    comparator = forms.CharField(max_length=50)
    int_value = forms.IntegerField(required=False)
    country = forms.CharField(max_length=100, required=False)
    subdivision = forms.CharField(max_length=100, required=False)
        
class hitForm(forms.ModelForm):
    class Meta:
        model = HIT
        fields = ['hit_id', 'hittype_id', 'assignments', 'expiry_date']

class hittypeForm(forms.ModelForm):
    class Meta:
        model = HITType
        fields = ['batch', 'title', 'hittype_id', 'description', 'keyword', 'reward', 'quals']
