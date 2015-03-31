# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_auto_20150310_0836'),
        ('task', '0007_task__fulfilled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='craftingtaskdirectory',
            name='material',
        ),
        migrations.AddField(
            model_name='craftingtaskdirectory',
            name='ingredient',
            field=models.ManyToManyField(to='item.ItemDirectory', through='item.ItemRecipe'),
            preserve_default=True,
        ),
    ]
