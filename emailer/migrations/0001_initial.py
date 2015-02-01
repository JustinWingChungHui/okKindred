# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email_type', models.CharField(choices=[('R', 'Self registration confirmation'), ('O', 'Other User registered me confirmation'), ('N', 'New Family Member'), ('U', 'Family Member Deatils Updated')], max_length=1, db_index=True)),
                ('recipient', models.EmailField(db_index=True, max_length=75)),
                ('subject', models.CharField(max_length=78)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('send_attempts', models.IntegerField(default=0)),
                ('send_successful', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email_type', models.CharField(choices=[('R', 'Self registration confirmation'), ('O', 'Other User registered me confirmation'), ('N', 'New Family Member'), ('U', 'Family Member Deatils Updated')], max_length=1, db_index=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('zh-hk', '繁體中文'), ('zh-cn', '简体中文'), ('pl', 'Polski'), ('fi', 'Suomi')], max_length=5, db_index=True)),
                ('subject', models.CharField(max_length=60, blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='emailtemplate',
            unique_together=set([('email_type', 'language')]),
        ),
    ]
