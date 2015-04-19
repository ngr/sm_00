# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(blank=True, max_length=127)),
                ('area', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('area_used', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationDirectory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=127)),
                ('area', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=127)),
                ('area', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='locationdirectory',
            name='type',
            field=models.ForeignKey(to='area.LocationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='design',
            field=models.ForeignKey(to='area.LocationDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(to='area.Region'),
            preserve_default=True,
        ),
    ]
