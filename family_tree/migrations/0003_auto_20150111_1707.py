# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0002_auto_20150111_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='large_thubnail',
            field=models.ImageField(upload_to='profile_photos', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='small_thumbnail',
            field=models.ImageField(upload_to='profile_photos', blank=True),
            preserve_default=True,
        ),
    ]
