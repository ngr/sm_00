# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0005_delete_skilltrainedmanager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilltrained',
            name='level',
        ),
        migrations.AddField(
            model_name='skilltrained',
            name='exp',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], default=1),
            preserve_default=True,
        ),
    ]
