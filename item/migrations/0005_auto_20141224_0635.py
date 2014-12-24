# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_auto_20141223_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodtype',
            name='itemdirectory_ptr',
        ),
        migrations.DeleteModel(
            name='FoodType',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='amount',
            new_name='_amount',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='date_expire',
            new_name='_date_expire',
        ),
    ]
