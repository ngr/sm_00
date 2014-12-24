# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_plant_yield_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='name',
            new_name='_name',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='primary_skill',
            new_name='_primary_skill',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='secondary_skill',
            new_name='_secondary_skill',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='yield_item',
            new_name='_yield_item',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='base_yield',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='exec_time',
        ),
        migrations.AddField(
            model_name='plant',
            name='_base_yield',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plant',
            name='_exec_time',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plant',
            name='_plantation_area',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
    ]
