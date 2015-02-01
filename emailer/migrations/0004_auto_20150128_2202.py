# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0003_auto_20150126_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='familynewsletterevents',
            name='family',
        ),
        migrations.RemoveField(
            model_name='familynewsletterevents',
            name='person',
        ),
        migrations.AddField(
            model_name='familynewsletterevents',
            name='family_id',
            field=models.IntegerField(null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='familynewsletterevents',
            name='person_id',
            field=models.IntegerField(null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='familynewsletterevents',
            name='person_name',
            field=models.CharField(null=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='familynewsletterevents',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
