# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0007_auto_20141224_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='area',
            new_name='_area',
        ),
        migrations.AddField(
            model_name='location',
            name='_name',
            field=models.CharField(default='', blank=True, max_length=127),
            preserve_default=False,
        ),
    ]
