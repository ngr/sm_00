# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20141223_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='_yield_item',
        ),
    ]
