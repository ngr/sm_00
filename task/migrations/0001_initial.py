# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slave', '0022_auto_20141212_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_start', models.DateTimeField(verbose_name='Time of task start')),
                ('date_finish', models.DateTimeField(verbose_name='Time of task finish')),
                ('retrieved', models.BooleanField(default=False)),
                ('slave', models.ForeignKey(to='slave.Slave')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
