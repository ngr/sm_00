# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0014_auto_20150105_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodstock',
            name='warehouse_ptr',
        ),
        migrations.DeleteModel(
            name='FoodStock',
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
    ]
