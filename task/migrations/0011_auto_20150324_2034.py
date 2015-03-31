# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_auto_20150324_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='_date_assigned',
            new_name='date_assigned',
        ),
        migrations.RenameField(
            model_name='assignment',
            old_name='_date_released',
            new_name='date_released',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='slave',
            field=models.ForeignKey(related_name='assignments', to='slave.Slave'),
            preserve_default=True,
        ),
    ]
