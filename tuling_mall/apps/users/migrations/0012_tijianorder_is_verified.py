# Generated by Django 3.2.23 on 2024-04-11 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_tijianorder_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='tijianorder',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='审核状态'),
        ),
    ]
