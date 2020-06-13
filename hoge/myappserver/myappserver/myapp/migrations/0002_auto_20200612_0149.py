# Generated by Django 2.2.13 on 2020-06-12 01:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointcloud',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pointcloud',
            name='x',
            field=models.CharField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='pointcloud',
            name='y',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='pointcloud',
            name='z',
            field=models.CharField(max_length=2000),
        ),
    ]
