# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0002_auto_20141213_2027'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='skilltrained',
            unique_together=set([('slave', 'skill')]),
        ),
    ]
