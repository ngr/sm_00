# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='_location',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='_owner',
            new_name='owner',
        ),
    ]
