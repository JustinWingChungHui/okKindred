# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0005_person_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biography',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('zh-hk', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish')], db_index=True, max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('zh-hk', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish')], default='en', max_length=5),
            preserve_default=True,
        ),
    ]
