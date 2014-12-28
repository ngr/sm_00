# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0015_auto_20141225_0952'),
        ('task', '0009_remove_plant__yield_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='_yield_item',
            field=models.ForeignKey(default=1, to='item.ItemDirectory'),
            preserve_default=False,
        ),
    ]
