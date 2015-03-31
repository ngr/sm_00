# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_auto_20150302_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemRecipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('_amount', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='itemmaterialrecipe',
            name='material',
        ),
        migrations.RemoveField(
            model_name='itemmaterialrecipe',
            name='task_type',
        ),
    ]
