# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0006_auto_20150221_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biography',
            name='language',
            field=models.CharField(max_length=5, choices=[('en', 'English'), ('zh-hk', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish'), ('fr', 'French')], db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='language',
            field=models.CharField(max_length=5, default='en', choices=[('en', 'English'), ('zh-hk', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish'), ('fr', 'French')]),
            preserve_default=True,
        ),
    ]
