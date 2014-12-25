# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0006_auto_20141223_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodstock',
            name='_food',
        ),
        migrations.RemoveField(
            model_name='foodstock',
            name='warehouse_ptr',
        ),
        migrations.DeleteModel(
            name='FoodStock',
        ),
    ]
