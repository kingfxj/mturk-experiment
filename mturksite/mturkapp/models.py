from django.db import models


# Create your models here.
class Assignments(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthYear = models.IntegerField()
    birthCity = models.CharField(max_length=100)

    class Meta:
        db_table = "mturk_app_assignments"
