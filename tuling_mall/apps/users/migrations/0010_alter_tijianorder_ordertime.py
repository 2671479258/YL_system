# Generated by Django 3.2.23 on 2024-04-09 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20240409_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tijianorder',
            name='ordertime',
            field=models.DateTimeField(null=True, verbose_name='预约时间'),
        ),
    ]
