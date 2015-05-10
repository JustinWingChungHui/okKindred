# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0006_email_content_html'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='familynewsletterevents',
            options={'verbose_name_plural': 'FamilyNewsLetterEvents'},
        ),
    ]
