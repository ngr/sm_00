# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(blank=True, max_length=127)),
                ('_amount', models.PositiveIntegerField(default=1)),
                ('_date_init', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemDirectory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('_name', models.CharField(default='', max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodDirectory',
            fields=[
                ('itemdirectory_ptr', models.OneToOneField(serialize=False, parent_link=True, to='item.ItemDirectory', primary_key=True, auto_created=True)),
                ('_taste', models.PositiveSmallIntegerField(default=1)),
                ('_satiety', models.PositiveSmallIntegerField(default=1)),
                ('_shelf_life', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=('item.itemdirectory',),
        ),
        migrations.CreateModel(
            name='ItemJoffreyList',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('execution_time', models.DateTimeField()),
                ('reason', models.CharField(blank=True, max_length=255)),
                ('item', models.ForeignKey(unique=True, to='item.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaterialDirectory',
            fields=[
                ('itemdirectory_ptr', models.OneToOneField(serialize=False, parent_link=True, to='item.ItemDirectory', primary_key=True, auto_created=True)),
                ('_density', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=('item.itemdirectory',),
        ),
        migrations.AddField(
            model_name='itemdirectory',
            name='_related',
            field=models.ManyToManyField(blank=True, to='item.ItemDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='_itype',
            field=models.ForeignKey(to='item.ItemDirectory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='_warehouse',
            field=models.ForeignKey(to='area.Warehouse'),
            preserve_default=True,
        ),
    ]
