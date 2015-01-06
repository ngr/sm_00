# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0016_auto_20150105_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='_building',
        ),
    ]
