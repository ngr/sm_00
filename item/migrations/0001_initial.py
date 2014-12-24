# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=127)),
                ('taste', models.PositiveSmallIntegerField(default=1)),
                ('shelf_life', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('itype', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('item_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, to='item.Item', primary_key=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('date_expire', models.DateTimeField()),
                ('food_type', models.ForeignKey(to='item.FoodType')),
            ],
            options={
            },
            bases=('item.item',),
        ),
    ]
