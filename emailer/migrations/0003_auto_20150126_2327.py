# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0005_person_language'),
        ('emailer', '0002_familynewsletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyNewsLetterEvents',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('new_member', models.BooleanField(default=False, db_index=True)),
                ('creation_date', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('family', models.ForeignKey(to='family_tree.Family')),
                ('person', models.ForeignKey(to='family_tree.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='EmailTemplate',
        ),
        migrations.DeleteModel(
            name='FamilyNewsLetter',
        ),
        migrations.RemoveField(
            model_name='email',
            name='email_type',
        ),
    ]
