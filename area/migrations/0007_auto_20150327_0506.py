# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0006_buildingmaterialrecipe_task_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmingfield',
            name='_area_used',
        ),
        migrations.AddField(
            model_name='location',
            name='_area_used',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
