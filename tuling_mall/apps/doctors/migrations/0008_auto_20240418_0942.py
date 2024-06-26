# Generated by Django 3.2.23 on 2024-04-18 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0007_healthrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthrecord',
            name='replied',
            field=models.BooleanField(default=False, verbose_name='是否已回复'),
        ),
        migrations.CreateModel(
            name='DoctorReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_diagnosis', models.CharField(max_length=200, verbose_name='健康诊断')),
                ('offline_medical_advice', models.CharField(choices=[('yes', '是'), ('no', '否')], max_length=3, verbose_name='是否建议线下就医')),
                ('health_analysis', models.TextField(verbose_name='健康分析')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctorinfo', verbose_name='医生')),
                ('health_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.healthrecord', verbose_name='健康记录')),
            ],
            options={
                'verbose_name': '医生回复',
                'verbose_name_plural': '医生回复',
                'db_table': 'tb_doctor_reply',
            },
        ),
    ]
