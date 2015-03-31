# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('task', '0003_auto_20150302_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='CraftingTaskDirectory',
            fields=[
                ('taskdirectory_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='task.TaskDirectory')),
                ('_work_units', models.PositiveIntegerField(default=1)),
                ('_yield_item', models.ForeignKey(to='item.ItemDirectory')),
                ('materials', models.ManyToManyField(related_name='crafting_materials', to='item.ItemDirectory')),
            ],
            options={
            },
            bases=('task.taskdirectory',),
        ),
        migrations.AlterField(
            model_name='taskdirectory',
            name='_location_type',
            field=models.CharField(max_length=127, choices=[('farmingfield', 'Farming Field'), ('housingdistrict', 'Housing District'), ('workshop', 'Workshop')], blank=True),
            preserve_default=True,
        ),
    ]
