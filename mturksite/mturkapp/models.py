from django.db import models


# Create your models here.
class Assignment(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthYear = models.IntegerField()
    birthCity = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    class Meta:
        # Remote database name
        db_table = "mturk_app_assignments"

class Qualification(models.Model):
    nickname = models.CharField(max_length=100)
    qualID = models.CharField(max_length=255, null=False)
    comparator = models.CharField(max_length=50)
    int_value = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    actions_guarded = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        #remote database name
        db_table = "mturk_app_qualifications"
        