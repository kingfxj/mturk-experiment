from .models import Assignment, HIT, HITType
from django.contrib import admin

# Register your models here.
admin.site.register(Assignment)
admin.site.register(HIT)
admin.site.register(HITType)