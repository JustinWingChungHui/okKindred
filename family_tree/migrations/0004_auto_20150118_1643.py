# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0003_auto_20150111_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='large_thubnail',
            new_name='large_thumbnail',
        ),
    ]
