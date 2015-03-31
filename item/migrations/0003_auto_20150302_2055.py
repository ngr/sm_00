# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20150302_2032'),
        ('item', '0002_itemmaterialrecipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemmaterialrecipe',
            name='item',
        ),
        migrations.AddField(
            model_name='itemmaterialrecipe',
            name='task_type',
            field=models.ForeignKey(to='task.CraftingTaskDirectory', related_name='task_type', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itemmaterialrecipe',
            name='material',
            field=models.ForeignKey(to='item.MaterialDirectory', related_name='material'),
            preserve_default=True,
        ),
    ]
