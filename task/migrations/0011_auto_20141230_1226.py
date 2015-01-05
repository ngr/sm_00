# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_auto_20141230_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='_primary_skill',
        ),
        migrations.RemoveField(
            model_name='task',
            name='_secondary_skill',
        ),
    ]
