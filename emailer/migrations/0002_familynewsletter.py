# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyNewsLetter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
