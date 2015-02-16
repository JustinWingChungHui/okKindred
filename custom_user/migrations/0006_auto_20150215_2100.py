# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0005_auto_20150125_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='receive_new_family_member_emails',
            field=models.BooleanField(default=True, verbose_name='Receive New Family Meber Emails', help_text='Sends out emails if a new family member has been added'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='receive_update_emails',
            field=models.BooleanField(default=True, verbose_name='Receive Update Emails', help_text='Sends out emails if a profile has been changed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(default='en', max_length=5, db_index=True, choices=[('en', 'English'), ('zh-hk', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish')]),
            preserve_default=True,
        ),
    ]
