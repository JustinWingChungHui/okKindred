# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0004_auto_20150118_1643'),
        ('custom_user', '0002_auto_20150111_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='family',
            field=models.ForeignKey(to='family_tree.Family', null=True),
            preserve_default=True,
        ),
    ]
