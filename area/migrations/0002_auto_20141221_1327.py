# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='name',
            field=models.CharField(default='Market', max_length=127),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='region',
            name='area',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
            preserve_default=True,
        ),
    ]
