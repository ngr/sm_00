# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0025_auto_20150109_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemjoffreylist',
            name='item',
            field=models.ForeignKey(to='item.Item', unique=True),
            preserve_default=True,
        ),
    ]
