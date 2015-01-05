# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20141230_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='_date_init',
            new_name='_date_start',
        ),
        migrations.AddField(
            model_name='task',
            name='_date_finish',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 19, 58, 26, 318429, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
