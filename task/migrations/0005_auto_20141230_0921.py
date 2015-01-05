# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0012_auto_20141228_1827'),
        ('task', '0004_task__type'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='_date_assigned',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 9, 21, 12, 669788, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='_date_released',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='_location',
            field=models.ForeignKey(default=1, to='area.Location'),
            preserve_default=False,
        ),
    ]
