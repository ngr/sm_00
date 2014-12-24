# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('area', '0004_auto_20141222_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(default='Warehouse', max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodStock',
            fields=[
                ('warehouse_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, to='area.Warehouse', primary_key=True)),
                ('expires', models.DateTimeField()),
                ('food', models.ForeignKey(to='item.Food')),
            ],
            options={
            },
            bases=('area.warehouse',),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='region',
            field=models.ForeignKey(to='area.Region'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='housingdistrict',
            name='beds',
        ),
    ]
