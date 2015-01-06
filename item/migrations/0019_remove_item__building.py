# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0018_item__building'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='_building',
        ),
    ]
