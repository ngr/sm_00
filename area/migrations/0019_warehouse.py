# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0018_auto_20150106_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('_type', models.CharField(max_length=127, choices=[('fooddirectory', 'Food'), ('materialdirectory', 'Material')])),
                ('_region', models.ForeignKey(to='area.Region')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
