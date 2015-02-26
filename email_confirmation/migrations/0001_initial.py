# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0006_auto_20150221_1503'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('email_address', models.EmailField(unique=True, max_length=75)),
                ('sent', models.DateTimeField(db_index=True)),
                ('confirmation_key', models.CharField(unique=True, db_index=True, max_length=40)),
                ('person', models.ForeignKey(unique=True, null=True, to='family_tree.Person')),
                ('user_who_invited_person', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
