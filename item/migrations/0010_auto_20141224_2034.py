# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0009_itemdirectory__itype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdirectory',
            name='_itype',
            field=models.ManyToManyField(related_name='_itype_rel_+', to='item.ItemDirectory', null=True),
            preserve_default=True,
        ),
    ]
