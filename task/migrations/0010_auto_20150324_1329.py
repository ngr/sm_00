# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20150320_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(related_name='assignments', to='task.Task'),
            preserve_default=True,
        ),
    ]
