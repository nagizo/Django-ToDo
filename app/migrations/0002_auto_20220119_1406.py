# Generated by Django 3.2.8 on 2022-01-19 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='end_time',
            field=models.TimeField(verbose_name='終了時間'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='start_time',
            field=models.TimeField(verbose_name='開始時間'),
        ),
    ]
