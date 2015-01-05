# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0006_auto_20141220_1425'),
        ('task', '0009_taskdirectory__location_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='_primary_skill',
            field=models.ForeignKey(to='skill.Skill', default=1, related_name='+'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='_secondary_skill',
            field=models.ManyToManyField(related_name='+', to='skill.Skill'),
            preserve_default=True,
        ),
    ]
