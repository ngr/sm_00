# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slave', '0025_slave_location'),
        ('task', '0007_remove_assignment_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='slave',
            field=models.ForeignKey(to='slave.Slave', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(to='task.Task', default=1),
            preserve_default=False,
        ),
    ]
