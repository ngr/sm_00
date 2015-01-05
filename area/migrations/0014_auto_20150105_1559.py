# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0013_auto_20150104_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='_building',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='_item',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='name',
            field=models.CharField(max_length=127, default='qwerty'),
            preserve_default=False,
        ),
    ]
