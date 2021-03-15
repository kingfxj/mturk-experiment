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

class HIT(models.Model):
    hit_id = models.CharField(max_length=100)
    hittype_id = models.CharField(max_length=100)
    assignments = models.IntegerField()
    expiry_date = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_hits"

class HITType(models.Model):
    batch = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    hittype_id = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    reward = models.CharField(max_length=100)
    quals = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_hittypes"
