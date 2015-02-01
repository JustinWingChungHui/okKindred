# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0005_remove_email_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='content_html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
