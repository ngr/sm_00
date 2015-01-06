# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0019_warehouse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='_type',
        ),
    ]
