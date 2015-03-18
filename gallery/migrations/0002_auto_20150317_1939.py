# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0007_auto_20150315_2358'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='family',
            field=models.ForeignKey(default=1, to='family_tree.Family'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gallery',
            name='creation_date',
            field=models.DateTimeField(db_index=True, auto_now_add=True),
            preserve_default=True,
        ),
    ]
