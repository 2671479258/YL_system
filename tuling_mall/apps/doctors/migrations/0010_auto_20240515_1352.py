# Generated by Django 3.2.23 on 2024-05-15 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0009_doctorinfo_doctor_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctororder',
            name='diet_habits',
            field=models.CharField(choices=[('是', '是'), ('否', '否')], max_length=10, null=True, verbose_name='是否规律饮食'),
        ),
        migrations.AddField(
            model_name='doctororder',
            name='exercise_habits',
            field=models.CharField(choices=[('是', '是'), ('否', '否')], max_length=10, null=True, verbose_name='是否定期运动'),
        ),
        migrations.AddField(
            model_name='doctororder',
            name='stay_up_late',
            field=models.CharField(choices=[('是', '是'), ('否', '否')], max_length=10, null=True, verbose_name='近期是否经常性熬夜'),
        ),
    ]