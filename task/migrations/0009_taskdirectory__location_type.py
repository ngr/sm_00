# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20141230_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdirectory',
            name='_location_type',
            field=models.CharField(choices=[('farmingfield', 'Farming Field'), ('housingdistrict', 'Housing District')], blank=True, max_length=127, default='farmingfield'),
            preserve_default=False,
        ),
    ]
