# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0002_auto_20141221_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='HousingDistrict',
            fields=[
                ('location_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='area.Location', auto_created=True)),
                ('beds', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=('area.location',),
        ),
    ]
