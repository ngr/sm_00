# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0010_auto_20141228_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='_building',
            field=models.ForeignKey(default=1, to='area.WarehouseBuilding'),
            preserve_default=False,
        ),
    ]
