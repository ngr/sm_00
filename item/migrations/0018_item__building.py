# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0017_warehousebuilding'),
        ('item', '0017_remove_item__building'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='_building',
            field=models.ForeignKey(to='area.WarehouseBuilding', default=1),
            preserve_default=False,
        ),
    ]
