# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20141217_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='primary_skill',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='secondary_skill',
        ),
    ]
