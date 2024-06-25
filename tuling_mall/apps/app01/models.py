from django.db import models



class AdminsInfo(models.Model):
    whousename=models.CharField(max_length=20,verbose_name='使用者姓名')
    username = models.CharField(max_length=20, verbose_name='管理员用户名')
    password = models.CharField(max_length=20, verbose_name='管理员密码')

    class Meta:
        app_label = 'app01'
        verbose_name='管理员账号'
        verbose_name_plural=verbose_name
        db_table='tb_admin'

    def __str__(self):
        return self.whousename

