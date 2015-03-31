# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(blank=True, max_length=127)),
                ('_area', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HousingDistrict',
            fields=[
                ('location_ptr', models.OneToOneField(serialize=False, parent_link=True, to='area.Location', primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=('area.location',),
        ),
        migrations.CreateModel(
            name='FarmingField',
            fields=[
                ('location_ptr', models.OneToOneField(serialize=False, parent_link=True, to='area.Location', primary_key=True, auto_created=True)),
                ('_area_used', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=('area.location',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(max_length=127)),
                ('area', models.BigIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_region', models.ForeignKey(to='area.Region')),
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
