# Generated by Django 3.1.7 on 2021-04-11 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mturkapp', '0002_gameresultmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qualification',
            old_name='qualificationTypeId',
            new_name='QualificationTypeId',
        ),
    ]
