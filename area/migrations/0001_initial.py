# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('area', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FarmingField',
            fields=[
                ('location_ptr', models.OneToOneField(to='area.Location', serialize=False, primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
            },
            bases=('area.location',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('area', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(to='area.Region'),
            preserve_default=True,
        ),
    ]
