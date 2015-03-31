# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemMaterialRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('_amount', models.PositiveIntegerField(default=1)),
                ('item', models.ForeignKey(to='item.ItemDirectory')),
                ('material', models.ForeignKey(to='item.MaterialDirectory', related_name='material_recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
