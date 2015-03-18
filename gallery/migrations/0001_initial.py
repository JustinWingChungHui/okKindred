# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models.image


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0007_auto_20150315_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=50, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('family', models.ForeignKey(to='family_tree.Family')),
            ],
            options={
                'verbose_name_plural': 'Galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('original_image', models.ImageField(blank=True, upload_to=gallery.models.image.upload_to)),
                ('thumbnail', models.ImageField(blank=True, upload_to=gallery.models.image.upload_to)),
                ('large_thumbnail', models.ImageField(blank=True, upload_to=gallery.models.image.upload_to)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('date_taken', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('latitude', models.FloatField(default=0, blank=True)),
                ('longitude', models.FloatField(default=0, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('gallery', models.ForeignKey(to='gallery.Gallery')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('x1', models.FloatField()),
                ('y1', models.FloatField()),
                ('x2', models.FloatField()),
                ('y2', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(to='gallery.Image')),
                ('person', models.ForeignKey(to='family_tree.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='gallery',
            unique_together=set([('title', 'family')]),
        ),
    ]
