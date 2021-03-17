from django.db import models
from django_countries.fields import CountryField

class Qualification(models.Model):   
    nickname = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True, null=False)
    qualID = models.CharField(max_length=255)
    comparator = models.CharField(max_length=50)
    int_value = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    Status = models.BooleanField(default= False)


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
