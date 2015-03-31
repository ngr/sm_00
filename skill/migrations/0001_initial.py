# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slave', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('primary_attribute', models.PositiveSmallIntegerField(choices=[(0, 'Intelligence'), (1, 'Strength'), (2, 'Agility'), (3, 'Charisma')])),
                ('difficulty', models.PositiveSmallIntegerField(default=1)),
                ('required_skills', models.ManyToManyField(to='skill.Skill', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillTrained',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('exp', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('skill', models.ForeignKey(to='skill.Skill')),
                ('slave', models.ForeignKey(to='slave.Slave')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='skilltrained',
            unique_together=set([('slave', 'skill')]),
        ),
    ]
