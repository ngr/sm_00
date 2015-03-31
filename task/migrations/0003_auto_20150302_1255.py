# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150302_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='_type',
            new_name='type',
        ),
    ]
