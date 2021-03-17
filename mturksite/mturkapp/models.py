from django.db import models


class Qualification(models.Model):
    nickname = models.CharField(max_length=100)
    qualID = models.CharField(max_length=255, null=False)
    comparator = models.CharField(max_length=50)
    int_value = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    actions_guarded = models.CharField(max_length=100, blank=True, null=True)
    Status = models.BooleanField(default= False)
    
    class Meta:
        # Remote database name
        db_table = "mturk_app_qualifications"


class HITType(models.Model):
    title = models.CharField(max_length=100)
    hittype_id = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    reward = models.CharField(max_length=100)
    quals = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_hittypes"


class HIT(models.Model):
   
    hit_id = models.CharField(max_length=100)
    hittype_id = models.CharField(max_length=100)
    max_assignments = models.IntegerField()
    expiry_time = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_hits"





