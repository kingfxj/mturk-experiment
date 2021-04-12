# Generated by Django 3.1.7 on 2021-04-12 01:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssignQualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.CharField(max_length=100)),
                ('qualifications', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AssignStatModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_id', models.CharField(blank=True, max_length=100)),
                ('hit_id', models.CharField(blank=True, max_length=100)),
                ('worker_id', models.CharField(blank=True, max_length=100)),
                ('flag', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'games_assignstatmodel',
            },
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_id', models.CharField(max_length=100)),
                ('worker_id', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('batch_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'mturk_app_experiments',
            },
        ),
        migrations.CreateModel(
            name='GameResultModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_id', models.CharField(blank=True, max_length=100)),
                ('hit_id', models.CharField(blank=True, max_length=100)),
                ('worker_id', models.CharField(blank=True, max_length=100)),
                ('data', models.JSONField()),
            ],
            options={
                'db_table': 'games_gameresultmodel',
            },
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hit_id', models.CharField(max_length=100)),
                ('hittype_id', models.CharField(max_length=100)),
                ('max_assignments', models.IntegerField()),
                ('lifetime_in_seconds', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'mturk_app_hits',
            },
        ),
        migrations.CreateModel(
            name='Hittype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(max_length=100)),
                ('batch_title', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('hittype_id', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('keyword', models.CharField(max_length=100)),
                ('reward', models.CharField(max_length=100)),
                ('qualifications', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'mturk_app_hittypes',
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=2000)),
                ('QualificationTypeId', models.CharField(max_length=255)),
                ('comparator', models.CharField(blank=True, max_length=50)),
                ('int_value', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('subdivision', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'mturk_app_qualifications',
            },
        ),
    ]
