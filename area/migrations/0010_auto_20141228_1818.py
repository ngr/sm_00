# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0009_auto_20141228_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(max_length=127)),
                ('_type', models.CharField(choices=[('fooddirectory', 'Food'), ('materialdirectory', 'Material')], max_length=127)),
                ('_region', models.ForeignKey(to='area.Region')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='_name',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='_region',
        ),
    ]
