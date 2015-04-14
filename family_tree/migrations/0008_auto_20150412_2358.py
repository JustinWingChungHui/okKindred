# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0007_auto_20150315_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='facebook',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='linkedin',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='occupation',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='skype_name',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='spoken_languages',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='twitter',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
