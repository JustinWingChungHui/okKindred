# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0008_auto_20150412_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_year',
            field=models.IntegerField(blank=True, default=0, db_index=True),
            preserve_default=True,
        ),
    ]
