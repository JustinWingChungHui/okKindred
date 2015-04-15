# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0008_remove_user_is_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='receive_photo_update_emails',
            field=models.BooleanField(default=True, verbose_name='Receive Photo Update Emails', help_text='Sends out emails you have been tagged in a photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(max_length=5, db_index=True, choices=[('en', 'English'), ('zh-hk', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish'), ('fr', 'French')], default='en'),
            preserve_default=True,
        ),
    ]
