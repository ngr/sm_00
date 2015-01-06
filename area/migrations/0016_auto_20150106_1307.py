# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0015_auto_20150105_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehousebuilding',
            name='_region',
        ),
        migrations.DeleteModel(
            name='WarehouseBuilding',
        ),
    ]
