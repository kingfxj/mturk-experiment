# Generated by Django 3.1.7 on 2021-03-18 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mturkapp', '0004_auto_20210318_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hit',
            old_name='expiry_time',
            new_name='lifetime_in_seconds',
        ),
    ]