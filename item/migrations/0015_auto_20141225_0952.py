# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0014_auto_20141224_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='_date_expire',
            new_name='_instance_date_expire',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='_extra_satiety',
            new_name='_instance_satiety',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='_extra_taste',
            new_name='_instance_taste',
        ),
    ]
