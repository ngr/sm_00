# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='area',
            new_name='_area',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='_owner',
            new_name='owner',
        ),
    ]
