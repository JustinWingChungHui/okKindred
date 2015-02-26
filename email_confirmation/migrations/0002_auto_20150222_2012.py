# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_confirmation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='confirmation_key',
            field=models.CharField(db_index=True, max_length=64, unique=True),
            preserve_default=True,
        ),
    ]
