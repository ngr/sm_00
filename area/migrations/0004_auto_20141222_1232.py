# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_housingdistrict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housingdistrict',
            name='beds',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
