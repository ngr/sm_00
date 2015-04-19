# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0001_initial'),
        ('item', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('area', '0001_initial'),
        ('slave', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date_assigned', models.DateTimeField()),
                ('date_released', models.DateTimeField(null=True)),
                ('slave', models.ForeignKey(to='slave.Slave', related_name='assignments')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingMaterialRecipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('_amount', models.PositiveIntegerField(default=1)),
                ('material', models.ForeignKey(to='item.MaterialDirectory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('_date_start', models.DateTimeField()),
                ('_date_finish', models.DateTimeField()),
                ('_retrieved', models.BooleanField(default=False)),
                ('_yield', models.FloatField(default=0.0)),
                ('_fulfilled', models.FloatField(default=0.0)),
                ('location', models.ForeignKey(to='area.Location')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tasks')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskDirectory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=127)),
                ('area_per_worker', models.PositiveIntegerField(default=1)),
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
                ('taskdirectory_ptr', models.OneToOneField(parent_link=True, serialize=False, to='task.TaskDirectory', auto_created=True, primary_key=True)),
                ('_base_yield', models.PositiveSmallIntegerField(default=1)),
                ('_exec_time', models.PositiveSmallIntegerField(default=1)),
                ('_yield_item', models.ForeignKey(to='item.ItemDirectory')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.CreateModel(
            name='CraftingTaskDirectory',
            fields=[
                ('taskdirectory_ptr', models.OneToOneField(parent_link=True, serialize=False, to='task.TaskDirectory', auto_created=True, primary_key=True)),
                ('_work_units', models.PositiveIntegerField(default=1)),
                ('ingredient', models.ManyToManyField(to='item.ItemDirectory', through='item.ItemRecipe')),
                ('item', models.ForeignKey(to='item.ItemDirectory', related_name='yeild_item')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.CreateModel(
            name='BuildingTaskDirectory',
            fields=[
                ('taskdirectory_ptr', models.OneToOneField(parent_link=True, serialize=False, to='task.TaskDirectory', auto_created=True, primary_key=True)),
                ('_work_units', models.PositiveIntegerField(default=1)),
                ('building', models.ForeignKey(to='area.LocationDirectory')),
                ('material', models.ManyToManyField(to='item.MaterialDirectory', through='task.BuildingMaterialRecipe')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.AddField(
            model_name='taskdirectory',
            name='_primary_skill',
            field=models.ForeignKey(to='skill.Skill', related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskdirectory',
            name='_secondary_skill',
            field=models.ManyToManyField(to='skill.Skill', related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskdirectory',
            name='location_type',
            field=models.ForeignKey(to='area.LocationDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.ForeignKey(to='task.TaskDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buildingmaterialrecipe',
            name='task_type',
            field=models.ForeignKey(to='task.BuildingTaskDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(to='task.Task', related_name='assignments'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('slave', 'date_released')]),
        ),
    ]
