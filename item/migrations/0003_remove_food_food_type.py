# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20141223_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='food_type',
        ),
    ]
