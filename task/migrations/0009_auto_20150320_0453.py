# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20150310_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(related_name='tasks', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
