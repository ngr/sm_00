# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_auto_20141224_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdirectory',
            name='_itype',
            field=models.ManyToManyField(related_name='_itype_rel_+', blank=True, to='item.ItemDirectory'),
            preserve_default=True,
        ),
    ]
