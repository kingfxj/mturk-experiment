from rest_framework import serializers
from .models import assignments

class assignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = assignments
        fields = ('name', 'surname', 'birthYear', 'birthCity')