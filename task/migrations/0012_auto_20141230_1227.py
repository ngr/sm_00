# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0006_auto_20141220_1425'),
        ('task', '0011_auto_20141230_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdirectory',
            name='_primary_skill',
            field=models.ForeignKey(related_name='+', to='skill.Skill', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskdirectory',
            name='_secondary_skill',
            field=models.ManyToManyField(related_name='+', to='skill.Skill'),
            preserve_default=True,
        ),
    ]
