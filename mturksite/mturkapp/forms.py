from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class QualificationForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, required=True)
    country = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Qualification 
        fields = ['nickname', 'description','comparator', 'int_value', 'subdivision']
       
class HitForm(forms.ModelForm):
    hittype = forms.CharField(max_length=254)
    class Meta:
        model = Hit
        fields = ['max_assignments', 'lifetime_in_seconds']

class HittypeForm(forms.ModelForm):
    qualifications = forms.CharField(max_length=200, required=True ,widget=forms.CheckboxSelectMultiple)
    batch = forms.CharField(max_length=200)
    Assignment_Duration_In_Seconds = forms.IntegerField(required=True)
    Auto_Approval_Delay_In_Seconds = forms.IntegerField(required=True)
    class Meta:
        model = Hittype
        fields = ['title', 'description', 'keyword', 'reward']

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['title']

class AssignQualForm(forms.Form):
    qualifications = forms.CharField(max_length=200, required=True ,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = AssignQualification
        fields = ['worker_id', 'qualifications']