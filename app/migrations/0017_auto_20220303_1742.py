# Generated by Django 3.1.14 on 2022-03-03 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0016_auto_20220303_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a', to='auth.permission'),
        ),
    ]
