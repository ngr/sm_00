# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_auto_20141224_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemdirectory',
            old_name='name',
            new_name='_name',
        ),
        migrations.RemoveField(
            model_name='itemdirectory',
            name='_itype',
        ),
        migrations.AddField(
            model_name='itemdirectory',
            name='_related',
            field=models.ManyToManyField(to='item.ItemDirectory', blank=True, related_name='_related_rel_+'),
            preserve_default=True,
        ),
    ]
