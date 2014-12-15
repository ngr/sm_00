# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0004_auto_20141213_2150'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SkillTrainedManager',
        ),
    ]
