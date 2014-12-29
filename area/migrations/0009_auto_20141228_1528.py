# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0015_auto_20141225_0952'),
        ('area', '0008_auto_20141226_0733'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodStock',
            fields=[
                ('warehouse_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='area.Warehouse', serialize=False)),
            ],
            options={
            },
            bases=('area.warehouse',),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='_item',
            field=models.ForeignKey(to='item.Item', default=1, unique=True),
            preserve_default=False,
        ),
    ]
