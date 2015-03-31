# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0004_auto_20150302_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingmaterialrecipe',
            name='building',
        ),
    ]
