# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0002_auto_20150302_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('location_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='area.Location', serialize=False)),
            ],
            options={
            },
            bases=('area.location',),
        ),
    ]
