from django.db import models
from django_countries.fields import CountryField
import uuid
from django.utils.translation import ugettext_lazy as _

class Qualification(models.Model):   
    nickname = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True, null=False)
    QualificationTypeId = models.CharField(max_length=255)
    comparator = models.CharField(max_length=50, blank=True)
    int_value = models.IntegerField(blank=True, null=True )
    country =  models.CharField(max_length=100, blank=True, null=True)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_qualifications"

class Hit(models.Model):
    hit_id = models.CharField(max_length=100)
    hittype_id = models.CharField(max_length=100)
    max_assignments = models.IntegerField()
    lifetime_in_seconds = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_hits"

class Hittype(models.Model):
    batch_id = models.CharField(max_length=100)
    batch_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    hittype_id = models.CharField(max_length=100 , null=False)
    description = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    reward = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)

    class Meta:
        # Remote database name
        db_table = "mturk_app_hittypes"

class Experiment(models.Model):
    batch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    
    class Meta:
        # Remote database name
        db_table = "mturk_app_experiments"

class AssignQualification(models.Model):
    worker_id = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)
