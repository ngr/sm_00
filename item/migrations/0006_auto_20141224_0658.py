# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_auto_20141224_0635'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodDirectory',
            fields=[
                ('itemdirectory_ptr', models.OneToOneField(to='item.ItemDirectory', auto_created=True, primary_key=True, parent_link=True, serialize=False)),
                ('_taste', models.PositiveSmallIntegerField(default=1)),
                ('_satiety', models.PositiveSmallIntegerField(default=1)),
                ('_shelf_life', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=('item.itemdirectory',),
        ),
        migrations.AddField(
            model_name='food',
            name='_itype',
            field=models.ForeignKey(to='item.FoodDirectory', default=1),
            preserve_default=False,
        ),
    ]
