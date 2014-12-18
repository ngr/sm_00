# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20141217_0607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='pr_skill',
            new_name='primary_skill',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='sec_skill',
            new_name='secondary_skill',
        ),
    ]
