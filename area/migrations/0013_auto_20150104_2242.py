# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0012_auto_20141228_1827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='name',
            new_name='_name',
        ),
    ]
