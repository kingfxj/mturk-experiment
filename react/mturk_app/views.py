from django.shortcuts import render

# Create your views here.
from .models import assignments
from .serializers import assignmentsSerializer
from rest_framework import generics

class assignmentsListCreate(generics.ListCreateAPIView):
    queryset = assignments.objects.all()
    serializer_class = assignmentsSerializer
