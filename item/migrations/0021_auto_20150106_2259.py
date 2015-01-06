# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0020_item__warehouse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='item_ptr',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.RemoveField(
            model_name='material',
            name='item_ptr',
        ),
        migrations.DeleteModel(
            name='Material',
        ),
    ]
