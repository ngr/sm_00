# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0005_delete_skilltrainedmanager'),
        ('task', '0005_auto_20141217_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='primary_skill',
            field=models.ForeignKey(related_name='+', to='skill.Skill', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plant',
            name='secondary_skill',
            field=models.ManyToManyField(related_name='+', to='skill.Skill'),
            preserve_default=True,
        ),
    ]
