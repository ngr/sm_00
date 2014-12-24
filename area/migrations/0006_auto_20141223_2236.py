# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0005_auto_20141223_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodstock',
            old_name='expires',
            new_name='_expires',
        ),
        migrations.RenameField(
            model_name='foodstock',
            old_name='food',
            new_name='_food',
        ),
        migrations.RenameField(
            model_name='warehouse',
            old_name='region',
            new_name='_region',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='name',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='_name',
            field=models.CharField(default='Warehouse item', max_length=127),
            preserve_default=True,
        ),
    ]
