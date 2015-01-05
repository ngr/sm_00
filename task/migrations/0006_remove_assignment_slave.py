# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20141230_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='slave',
        ),
    ]
