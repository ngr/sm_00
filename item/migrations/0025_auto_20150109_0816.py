# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0024_itemjoffreylist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemjoffreylist',
            old_name='exec_time',
            new_name='execution_time',
        ),
    ]
