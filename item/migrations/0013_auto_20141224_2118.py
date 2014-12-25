# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0012_auto_20141224_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdirectory',
            name='_related',
            field=models.ManyToManyField(blank=True, to='item.ItemDirectory'),
            preserve_default=True,
        ),
    ]
