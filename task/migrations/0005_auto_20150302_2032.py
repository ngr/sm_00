# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20150302_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='craftingtaskdirectory',
            old_name='_yield_item',
            new_name='item',
        ),
        migrations.RemoveField(
            model_name='craftingtaskdirectory',
            name='materials',
        ),
    ]
