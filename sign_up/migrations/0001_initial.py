# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')])),
                ('language', models.CharField(max_length=5, choices=[('en', 'English'), ('zh-tw', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish'), ('fr', 'French')], default='en')),
                ('email_address', models.EmailField(max_length=75, unique=True)),
                ('confirmation_key', models.CharField(db_index=True, max_length=64, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
