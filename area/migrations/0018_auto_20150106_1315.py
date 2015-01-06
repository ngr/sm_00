# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0019_remove_item__building'),
        ('area', '0017_warehousebuilding'),
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
