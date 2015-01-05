# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_auto_20141230_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='_yield',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
