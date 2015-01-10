# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import family_tree.models.person


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=5, db_index=True, choices=[('en', 'English'), ('zh-hk', '繁體中文'), ('zh-cn', '简体中文'), ('pl', 'Polski'), ('fi', 'Suomi')])),
                ('content', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Biographies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Families',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, db_index=True, unique=True)),
                ('gender', models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')])),
                ('locked', models.BooleanField(default=False)),
                ('birth_year', models.IntegerField(default=0, blank=True)),
                ('year_of_death', models.IntegerField(default=0, blank=True)),
                ('photo', models.ImageField(upload_to='profile_photos', blank=True)),
                ('email', family_tree.models.person.NullableEmailField(default=None, max_length=75, blank=True, unique=True, null=True)),
                ('telephone_number', models.CharField(max_length=30, blank=True)),
                ('website', models.CharField(max_length=100, blank=True)),
                ('address', models.CharField(max_length=255, blank=True)),
                ('latitude', models.FloatField(default=0, blank=True)),
                ('longitude', models.FloatField(default=0, blank=True)),
                ('hierarchy_score', models.IntegerField(default=100, db_index=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('family', models.ForeignKey(to='family_tree.Family')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'People',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('relation_type', models.IntegerField(choices=[(1, 'Partnered'), (2, 'Raised'), (3, 'Raised By')])),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('from_person', models.ForeignKey(to='family_tree.Person', related_name='from_person')),
                ('to_person', models.ForeignKey(to='family_tree.Person', related_name='to_person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together=set([('from_person', 'to_person')]),
        ),
        migrations.AddField(
            model_name='biography',
            name='person',
            field=models.ForeignKey(to='family_tree.Person'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='biography',
            unique_together=set([('person', 'language')]),
        ),
    ]
