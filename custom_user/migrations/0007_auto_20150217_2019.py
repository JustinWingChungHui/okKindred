# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0006_auto_20150215_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='receive_new_family_member_emails',
        ),
        migrations.AlterField(
            model_name='user',
            name='receive_update_emails',
            field=models.BooleanField(verbose_name='Receive Update Emails', help_text='Sends out emails if family has been updated', default=True),
            preserve_default=True,
        ),
    ]
