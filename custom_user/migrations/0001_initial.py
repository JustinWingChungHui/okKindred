# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=75, verbose_name='Email Address', unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True, unique=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='Staff status')),
                ('is_superuser', models.BooleanField(help_text='Designates whether the user is superuser', default=False, verbose_name='Superuser')),
                ('is_confirmed', models.BooleanField(help_text='Designates whether the user has confirmed their membership', default=False, verbose_name='Confirmed')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='Active')),
                ('date_joined', models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
    ]
