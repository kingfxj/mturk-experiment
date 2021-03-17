from django.db import models

COMPARATOR_CHOICES = [
    ('select', 'SELECT CHOICE'),
    ('gt', 'greater than'),
    ('gte', 'greater than or equal to'),
    ('lt', 'less than'),
    ('lte', 'less than or eqaul to'),
    ('is_choice', 'is'),
    ('is_one', 'is one of'),
    ('is_not', 'is not'),
    ('is_not_one', 'is not one of'),
]

class Qualification(models.Model):   
    nickname = models.CharField(max_length=100)
    qualID = models.CharField(max_length=255, null=False)
    comparator = models.CharField(max_length=50)
    # comparator = models.CharField(max_length=50, choices=COMPARATOR_CHOICES, default=1)
    int_value = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    actions_guarded = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        # Remote database name
        db_table = "mturk_app_qualifications"

# class Qualification(models.Model):   
    # nickname = models.CharField(max_length=100)
    # qualID = models.CharField(max_length=255, null=False)
    # comparator = models.CharField(max_length=50)
    # # comparator = models.CharField(max_length=50, choices=COMPARATOR_CHOICES, default=1)
    # int_value = models.IntegerField(blank=True, null=True)
    # country = models.CharField(max_length=100, blank=True, null=True)
    # subdivision = models.CharField(max_length=100, blank=True, null=True)
    # actions_guarded = models.CharField(max_length=100, blank=True, null=True)
    # pass
    # class Meta:
    #     # Remote database name
    #     db_table = "mturk_app_qualifications"
        

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
