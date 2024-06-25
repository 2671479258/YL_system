from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel

# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True)
    real_name=models.CharField(max_length=10,null=True,verbose_name='真名')
    email_active=models.BooleanField(default=False,verbose_name='邮箱激活状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')
    allergy_history = models.CharField(max_length=100, default='0', verbose_name='过敏史')
    family_genetic_disease_history = models.CharField(max_length=100, default='0', verbose_name='家族遗传病史')
    class Meta:
        app_label = 'users'
        db_table='tb_users'
        verbose_name='用户管理'
        verbose_name_plural=verbose_name

    def set_password(self, raw_password):
        # 存储密码为明文形式
        self.password = raw_password

    def check_password(self, raw_password):
        # 直接比较密码明文
        return self.password == raw_password

    def save(self, *args, **kwargs):
        # 如果需要保存实例时进行其他操作，可以在这里添加
        super().save(*args, **kwargs)

    def __str__(self):
        return self.real_name




class Tijian(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='测试人')
    tijian_Data=models.DateField(verbose_name='体检时间',default='无数据')
    height=models.CharField(max_length=15,verbose_name='身高',default='无数据')
    weight=models.CharField(max_length=15,verbose_name='体重',default='无数据')
    lefteye=models.CharField(max_length=8,verbose_name='左眼视力',default='无数据')
    righteye=models.CharField(max_length=8,verbose_name='右眼视力',default='无数据')
    blood_pressure = models.CharField(max_length=15, verbose_name='血压', default='无数据')
    heart_rate = models.CharField(max_length=15, verbose_name='心率', default='无数据')
    blood_oxygen = models.CharField(max_length=15, verbose_name='血氧饱和度', default='无数据')


    class Meta:
        db_table='tb_tj'
        verbose_name='体检记录管理'
        verbose_name_plural=verbose_name



# 地址模型
class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    # PROTECT 当前字段受保护 不允许删除
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

class TijianOrder(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='预约用户')
    checkupType = models.CharField(max_length=40, verbose_name='预约类型')
    orderDate = models.DateField(verbose_name='预约日期', null=True)
    orderTime = models.TimeField(verbose_name='预约时间', null=True)
    ordertip = models.CharField(max_length=100, verbose_name='预约信息')
    allergy = models.CharField(null=True, max_length=10, verbose_name='过敏史', default='无')
    familyHistory = models.CharField(null=True, max_length=10, verbose_name='家族遗传病史', default='无')
    additionalInfo = models.TextField(verbose_name='额外信息', blank=True, null=True)
    xRay = models.BooleanField(verbose_name='X光', default=False)
    bloodTest = models.BooleanField(verbose_name='血液检查', default=False)
    urineTest = models.BooleanField(verbose_name='尿液检查', default=False)
    totalPrice = models.IntegerField(verbose_name='总价格', default=0)
    institution = models.CharField(max_length=50, verbose_name='到访机构', default=0)
    is_verified = models.BooleanField(verbose_name='审核状态', default=False)

    class Meta:
        db_table = 'tb_tj_order'
        verbose_name = '体检预约'
        verbose_name_plural = verbose_name