# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_itemmaterialrecipe'),
        ('area', '0003_workshop'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingMaterialRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('_amount', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('_name', models.CharField(max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='buildingmaterialrecipe',
            name='building',
            field=models.ForeignKey(to='area.BuildingType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buildingmaterialrecipe',
            name='material',
            field=models.ForeignKey(to='item.MaterialDirectory'),
            preserve_default=True,
        ),
    ]
