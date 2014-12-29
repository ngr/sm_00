# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slave', '0025_slave_location'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slave', models.ManyToManyField(to='slave.Slave')),
                ('task', models.ManyToManyField(to='task.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
