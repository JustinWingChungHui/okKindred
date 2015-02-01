# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0004_auto_20150128_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='creation_date',
        ),
    ]
