# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='required_skills',
            field=models.ManyToManyField(null=True, to='skill.Skill'),
            preserve_default=True,
        ),
    ]
