# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_remove_food_food_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodtype',
            name='id',
        ),
        migrations.RemoveField(
            model_name='foodtype',
            name='name',
        ),
        migrations.AddField(
            model_name='foodtype',
            name='itemdirectory_ptr',
            field=models.OneToOneField(serialize=False, auto_created=True, default=1, to='item.ItemDirectory', parent_link=True, primary_key=True),
            preserve_default=False,
        ),
    ]
