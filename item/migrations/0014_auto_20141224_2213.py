# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0013_auto_20141224_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('item_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='item.Item', auto_created=True)),
                ('_date_expire', models.DateTimeField(null=True)),
                ('_extra_taste', models.PositiveIntegerField(default=0)),
                ('_extra_satiety', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=('item.item',),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('item_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='item.Item', auto_created=True)),
                ('_density', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=('item.item',),
        ),
        migrations.AddField(
            model_name='item',
            name='_date_init',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 24, 22, 13, 17, 596204, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='_name',
            field=models.CharField(default='SomeItem', max_length=127),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='_amount',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
