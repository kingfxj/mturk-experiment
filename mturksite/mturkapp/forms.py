from django import forms
from .models import Assignments


class assignmentForm(forms.ModelForm):
    class Meta:
        model = Assignments
        fields = ["name", "surname", "birthYear", "birthCity"]
