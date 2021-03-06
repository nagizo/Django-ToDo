# Generated by Django 3.2.8 on 2022-01-21 01:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220119_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='end_time',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='終了時間'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='start_time',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='開始時間'),
        ),
    ]
