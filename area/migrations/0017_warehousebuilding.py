# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0016_auto_20150106_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_name', models.CharField(max_length=127)),
                ('_region', models.ForeignKey(to='area.Region')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
