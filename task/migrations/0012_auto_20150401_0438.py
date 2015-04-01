# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_auto_20150324_2034'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('slave', 'date_released')]),
        ),
    ]
