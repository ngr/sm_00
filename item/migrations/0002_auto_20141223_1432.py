# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDirectory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(default='', max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(default='', max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='itemdirectory',
            name='itype',
            field=models.ForeignKey(to='item.ItemType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='itype',
            field=models.ForeignKey(to='item.ItemDirectory'),
            preserve_default=True,
        ),
    ]
