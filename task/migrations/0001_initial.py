# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('skill', '0001_initial'),
        ('area', '0001_initial'),
        ('slave', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_date_assigned', models.DateTimeField()),
                ('_date_released', models.DateTimeField(null=True)),
                ('slave', models.ForeignKey(to='slave.Slave')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_date_start', models.DateTimeField()),
                ('_date_finish', models.DateTimeField()),
                ('_retrieved', models.BooleanField(default=False)),
                ('_yield', models.FloatField(default=0.0)),
                ('_location', models.ForeignKey(to='area.Location')),
                ('_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskDirectory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(max_length=127)),
                ('_location_type', models.CharField(blank=True, choices=[('farmingfield', 'Farming Field'), ('housingdistrict', 'Housing District')], max_length=127)),
                ('_area_per_worker', models.PositiveIntegerField(default=1)),
                ('_min_slaves', models.PositiveIntegerField(default=1)),
                ('_max_slaves', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FarmingTaskDirectory',
            fields=[
                ('taskdirectory_ptr', models.OneToOneField(serialize=False, parent_link=True, to='task.TaskDirectory', primary_key=True, auto_created=True)),
                ('_base_yield', models.PositiveSmallIntegerField(default=1)),
                ('_exec_time', models.PositiveSmallIntegerField(default=1)),
                ('_yield_item', models.ForeignKey(to='item.ItemDirectory')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.AddField(
            model_name='taskdirectory',
            name='_primary_skill',
            field=models.ForeignKey(related_name='+', to='skill.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskdirectory',
            name='_secondary_skill',
            field=models.ManyToManyField(related_name='+', to='skill.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='_type',
            field=models.ForeignKey(to='task.TaskDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(to='task.Task'),
            preserve_default=True,
        ),
    ]
