# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20141217_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='secondary_skill',
            field=models.ForeignKey(to='skill.Skill', related_name='+'),
            preserve_default=True,
        ),
    ]
