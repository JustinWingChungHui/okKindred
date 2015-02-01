# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0004_auto_20150118_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('zh-hk', '繁體中文'), ('zh-cn', '简体中文'), ('pl', 'Polski'), ('fi', 'Suomi')], default='en', max_length=5),
            preserve_default=True,
        ),
    ]
