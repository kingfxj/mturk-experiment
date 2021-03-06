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
