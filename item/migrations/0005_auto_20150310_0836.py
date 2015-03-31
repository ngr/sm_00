# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20150310_0836'),
        ('item', '0004_auto_20150310_0836'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ItemMaterialRecipe',
        ),
        migrations.AddField(
            model_name='itemrecipe',
            name='ingredient',
            field=models.ForeignKey(to='item.ItemDirectory', related_name='ingredient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemrecipe',
            name='task_type',
            field=models.ForeignKey(to='task.CraftingTaskDirectory', related_name='task_type'),
            preserve_default=True,
        ),
    ]
