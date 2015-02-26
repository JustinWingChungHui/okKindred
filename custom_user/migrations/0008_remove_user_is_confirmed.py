# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0007_auto_20150217_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_confirmed',
        ),
    ]
