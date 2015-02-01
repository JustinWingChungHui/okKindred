# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_user_family'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(max_length=5, choices=[('en', 'English'), ('zh-hk', '繁體中文'), ('zh-cn', '简体中文'), ('pl', 'Polski'), ('fi', 'Suomi')], default='en'),
            preserve_default=False,
        ),
    ]
