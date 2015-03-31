# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20150302_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='_fulfilled',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
