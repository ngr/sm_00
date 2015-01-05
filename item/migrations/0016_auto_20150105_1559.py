# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0014_auto_20150105_1559'),
        ('item', '0015_auto_20141225_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='_building',
            field=models.ForeignKey(default=1, to='area.WarehouseBuilding'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='_name',
            field=models.CharField(max_length=127, blank=True),
            preserve_default=True,
        ),
    ]
