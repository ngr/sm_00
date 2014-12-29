# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0015_auto_20141225_0952'),
        ('skill', '0006_auto_20141220_1425'),
        ('task', '0002_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(max_length=127)),
                ('_base_yield', models.PositiveSmallIntegerField(default=1)),
                ('_exec_time', models.PositiveSmallIntegerField(default=1)),
                ('_plantation_area', models.PositiveSmallIntegerField(default=1)),
                ('_primary_skill', models.ForeignKey(related_name='+', to='skill.Skill')),
                ('_secondary_skill', models.ManyToManyField(related_name='+', to='skill.Skill')),
                ('_yield_item', models.ForeignKey(to='item.ItemDirectory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskDirectory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(max_length=127)),
                ('_exec_time', models.PositiveIntegerField(default=1)),
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
                ('taskdirectory_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to='task.TaskDirectory', parent_link=True)),
                ('_plant', models.ForeignKey(to='task.Plant')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.RemoveField(
            model_name='task',
            name='_type',
        ),
        migrations.DeleteModel(
            name='TaskType',
        ),
    ]
