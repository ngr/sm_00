# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('task', '0006_auto_20141217_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='yield_item',
            field=models.ForeignKey(to='item.Item', default=1),
            preserve_default=False,
        ),
    ]
