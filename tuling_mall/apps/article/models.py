from django.db import models
from doctors.models import DoctorInfo

# Create your models here.
class Article_category(models.Model):
    category_name = models.CharField(max_length=10, verbose_name='文章类型')
    class Meta:
        app_label = 'article'
        verbose_name='文章类别'
        verbose_name_plural=verbose_name
        db_table='tb_article_category'
    def __str__(self):
        return self.category_name



class article(models.Model):
    title=models.CharField(max_length=20,verbose_name='文章标题')
    category=models.ForeignKey(Article_category,on_delete=models.CASCADE,verbose_name='所属类型')
    doctor=models.ForeignKey(DoctorInfo,on_delete=models.CASCADE,verbose_name='作者')
    introd=models.CharField(max_length=50,verbose_name='文章简介')
    content=models.TextField(max_length=2000,verbose_name='文章内容')
    release_data=models.DateField(verbose_name='发布日期')

    class Meta:
        app_label = 'article'
        verbose_name='文章'
        verbose_name_plural=verbose_name
        db_table='tb_article'

    def __str__(self):
        return self.title

