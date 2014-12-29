# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20141229_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='_type',
            field=models.ForeignKey(default=1, to='task.TaskDirectory'),
            preserve_default=False,
        ),
    ]
