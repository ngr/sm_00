# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0023_auto_20150108_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemJoffreyList',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('exec_time', models.DateTimeField()),
                ('reason', models.CharField(max_length=255, blank=True)),
                ('item', models.ForeignKey(to='item.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
