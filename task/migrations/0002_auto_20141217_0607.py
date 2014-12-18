# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0005_delete_skilltrainedmanager'),
        ('slave', '0022_auto_20141212_0742'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farming',
            fields=[
                ('task_ptr', models.OneToOneField(serialize=False, auto_created=True, to='task.Task', parent_link=True, primary_key=True)),
            ],
            options={
            },
            bases=('task.task',),
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('base_yield', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('exec_time', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('pr_skill', models.ManyToManyField(related_name='+', to='skill.Skill')),
                ('sec_skill', models.ForeignKey(related_name='+', to='skill.Skill', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RunningTask',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_finish', models.DateTimeField(verbose_name='Time of task finish', db_index=True)),
                ('slave', models.ForeignKey(related_name='+', to='slave.Slave')),
                ('task', models.ForeignKey(to='task.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='farming',
            name='plant',
            field=models.ForeignKey(to='task.Plant'),
            preserve_default=True,
        ),
    ]
