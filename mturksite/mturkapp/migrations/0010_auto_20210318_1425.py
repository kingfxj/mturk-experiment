# Generated by Django 3.1.7 on 2021-03-18 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mturkapp', '0009_hittype_batch_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hittype',
            old_name='batch_name',
            new_name='batch_title',
        ),
    ]