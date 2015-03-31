# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20150302_2055'),
        ('area', '0005_remove_buildingmaterialrecipe_building'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingmaterialrecipe',
            name='task_type',
            field=models.ForeignKey(to='task.BuildingTaskDirectory', default=1),
            preserve_default=False,
        ),
    ]
