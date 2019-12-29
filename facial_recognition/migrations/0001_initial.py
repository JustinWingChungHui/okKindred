# Generated by Django 2.2.6 on 2019-10-11 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('family_tree', '0014_auto_20191004_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceModel',
            fields=[
                ('family', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='family_tree.Family')),
                ('fit_data_faces', models.BinaryField()),
                ('fit_data_person_ids', models.BinaryField()),
                ('n_neighbors', models.IntegerField()),
                ('trained_knn_model', models.BinaryField()),
            ],
        ),
    ]