# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0021_auto_20150106_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdirectory',
            name='_related',
            field=models.ManyToManyField(related_name='_related_rel_+', to='item.ItemDirectory', blank=True),
            preserve_default=True,
        ),
    ]
