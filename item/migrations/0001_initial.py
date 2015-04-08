# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_name', models.CharField(max_length=127, blank=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_name', models.CharField(max_length=127, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodDirectory',
            fields=[
                ('itemdirectory_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='item.ItemDirectory', primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('execution_time', models.DateTimeField()),
                ('reason', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_amount', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaterialDirectory',
            fields=[
                ('itemdirectory_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='item.ItemDirectory', primary_key=True)),
                ('_density', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=('item.itemdirectory',),
        ),
        migrations.AddField(
            model_name='itemrecipe',
            name='ingredient',
            field=models.ForeignKey(to='item.ItemDirectory', related_name='ingredient'),
            preserve_default=True,
        ),
    ]
