# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_auto_20150302_2055'),
        ('area', '0005_remove_buildingmaterialrecipe_building'),
        ('task', '0005_auto_20150302_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingTaskDirectory',
            fields=[
                ('taskdirectory_ptr', models.OneToOneField(auto_created=True, to='task.TaskDirectory', primary_key=True, serialize=False, parent_link=True)),
                ('_work_units', models.PositiveIntegerField(default=1)),
                ('building', models.ForeignKey(to='area.BuildingType')),
                ('material', models.ManyToManyField(to='item.MaterialDirectory', through='area.BuildingMaterialRecipe')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.AddField(
            model_name='craftingtaskdirectory',
            name='material',
            field=models.ManyToManyField(to='item.MaterialDirectory', through='item.ItemMaterialRecipe'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='craftingtaskdirectory',
            name='item',
            field=models.ForeignKey(to='item.ItemDirectory', related_name='yeild_item'),
            preserve_default=True,
        ),
    ]
