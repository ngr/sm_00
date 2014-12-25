# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_auto_20141224_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialDirectory',
            fields=[
                ('itemdirectory_ptr', models.OneToOneField(to='item.ItemDirectory', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('_density', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=('item.itemdirectory',),
        ),
        migrations.RemoveField(
            model_name='food',
            name='_itype',
        ),
        migrations.RemoveField(
            model_name='food',
            name='item_ptr',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='itype',
            new_name='_itype',
        ),
        migrations.RenameField(
            model_name='itemdirectory',
            old_name='itype',
            new_name='_itype',
        ),
        migrations.AddField(
            model_name='item',
            name='_amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
