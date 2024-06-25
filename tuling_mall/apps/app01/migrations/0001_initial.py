# Generated by Django 3.2.23 on 2024-01-28 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whousename', models.CharField(max_length=20, verbose_name='使用者姓名')),
                ('username', models.CharField(max_length=20, verbose_name='管理员用户名')),
                ('password', models.CharField(max_length=20, verbose_name='管理员密码')),
            ],
            options={
                'verbose_name': '管理员账号',
                'verbose_name_plural': '管理员账号',
                'db_table': 'tb_admin',
            },
        ),
    ]