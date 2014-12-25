# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_auto_20141224_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdirectory',
            name='_itype',
        ),
        migrations.DeleteModel(
            name='ItemType',
        ),
    ]
