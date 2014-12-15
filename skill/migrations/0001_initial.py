# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slave', '0022_auto_20141212_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=127)),
                ('primary_attribute', models.PositiveSmallIntegerField(choices=[(0, 'Intelligence'), (1, 'Strength'), (2, 'Agility'), (3, 'Charisma')])),
                ('difficulty', models.PositiveSmallIntegerField(default=1)),
                ('required_skills', models.ManyToManyField(to='skill.Skill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillTrained',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('level', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], default=1)),
                ('skill', models.ForeignKey(to='skill.Skill')),
                ('slave', models.ForeignKey(to='slave.Slave')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
