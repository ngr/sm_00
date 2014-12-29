# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0011_warehouse__building'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='warehousebuilding',
            unique_together=set([('_region', '_type')]),
        ),
    ]
