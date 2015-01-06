# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0019_warehouse'),
        ('item', '0019_remove_item__building'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='_warehouse',
            field=models.ForeignKey(to='area.Warehouse', default=1),
            preserve_default=False,
        ),
    ]
