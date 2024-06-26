# Generated by Django 3.2.23 on 2024-03-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_auto_20240130_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctororder',
            name='allergy',
            field=models.CharField(choices=[('有', '有'), ('无', '无')], max_length=10, null=True, verbose_name='过敏史'),
        ),
        migrations.AddField(
            model_name='doctororder',
            name='familyHistory',
            field=models.CharField(choices=[('有', '有'), ('无', '无')], max_length=10, null=True, verbose_name='家族遗传病史'),
        ),
    ]
