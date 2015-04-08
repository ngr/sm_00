# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingMaterialRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_amount', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_name', models.CharField(max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_name', models.CharField(max_length=127, blank=True)),
                ('_area', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('_area_used', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HousingDistrict',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='area.Location', primary_key=True)),
            ],
            options={
            },
            bases=('area.location',),
        ),
        migrations.CreateModel(
            name='FarmingField',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='area.Location', primary_key=True)),
            ],
            options={
            },
            bases=('area.location',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_name', models.CharField(max_length=127)),
                ('_area', models.BigIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='area.Location', primary_key=True)),
            ],
            options={
            },
            bases=('area.location',),
        ),
    ]
