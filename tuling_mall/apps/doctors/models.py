from django.db import models

# Create your models here.
from django.db import models

from users.models import User


class Department(models.Model):
    department_name=models.CharField(max_length=10,verbose_name='科室名称')
    department_area=models.CharField(max_length=10,verbose_name='科室地址',null=True)
    department_introduce=models.CharField(max_length=30,verbose_name='科室简介',null=True)
    def __str__(self):
        return self.department_name



from enum import Enum

class DoctorTitle(Enum):
    RESIDENT_DOCTOR = '住院医师'
    ATTENDING_PHYSICIAN = '主治医师'
    ASSOCIATE_CHIEF_PHYSICIAN = '副主任医师'
    CHIEF_PHYSICIAN = '主任医师'

class DoctorInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name='医生用户名')
    doctorname = models.CharField(max_length=20, verbose_name='医生真名')
    password = models.CharField(max_length=20, verbose_name='医生账号密码')
    which_department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属科室')
    introducation = models.CharField(max_length=200, verbose_name='医生资料')
    doctor_image = models.ImageField(upload_to='media/doctor_images/', blank=True, null=True, verbose_name='医生图片')
    doctor_title = models.CharField(null=True,max_length=20, choices=[(tag.value, tag.value) for tag in DoctorTitle], verbose_name='医生职称')

    class Meta:
        app_label = 'doctors'
        verbose_name = '医生'
        verbose_name_plural = verbose_name
        db_table = 'tb_doctor'

    def __str__(self):
        return self.username

class DoctorOrder(models.Model):
    doctorname = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, verbose_name='预约医生')
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='预约用户')
    ordertime = models.CharField(max_length=40, verbose_name='预约时间')
    ordertip = models.CharField(max_length=100, verbose_name='预约信息')
    allergy = models.CharField(null=True, max_length=10, verbose_name='过敏史', choices=(('有', '有'), ('无', '无')))
    familyHistory = models.CharField(null=True, max_length=10, verbose_name='家族遗传病史', choices=(('有', '有'), ('无', '无')))
    mobile_phone = models.CharField(max_length=11, null=True)
    is_verified = models.BooleanField(verbose_name='审核状态', default=False)

    # 新增字段
    diet_habits = models.CharField(null=True, max_length=10, verbose_name='是否规律饮食', choices=(('是', '是'), ('否', '否')))
    exercise_habits = models.CharField(null=True, max_length=10, verbose_name='是否定期运动', choices=(('是', '是'), ('否', '否')))
    stay_up_late = models.CharField(null=True, max_length=10, verbose_name='近期是否经常性熬夜', choices=(('是', '是'), ('否', '否')))
    consultation_fee = models.DecimalField(null=True,max_digits=6, decimal_places=2, verbose_name='咨询费用')

    class Meta:
        db_table = 'tb_doctor_order'
        verbose_name = '医生预约'
        verbose_name_plural = verbose_name

class HealthRecord(models.Model):

    username=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='预约用户')
    doctorname = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, verbose_name='预约医生')

    current_time = models.DateTimeField()

    # 自测的一些身体数据
    blood_pressure = models.CharField(max_length=50, blank=True, null=True)
    body_temperature = models.CharField(max_length=50, blank=True, null=True)
    heart_rate = models.CharField(max_length=50, blank=True, null=True)
    blood_sugar = models.CharField(max_length=50, blank=True, null=True)
    body_weight = models.CharField(max_length=50, blank=True, null=True)
    body_height = models.CharField(max_length=50, blank=True, null=True)
    blood_oxygen = models.CharField(max_length=50, blank=True, null=True)

    # 身体状况
    no_symptoms = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    fever = models.BooleanField(default=False)
    cough = models.BooleanField(default=False)
    chest_pain = models.BooleanField(default=False)
    abdominal_pain = models.BooleanField(default=False)
    nausea = models.BooleanField(default=False)
    vomiting = models.BooleanField(default=False)
    other_symptoms = models.TextField(blank=True, null=True)

    # 其他身体状况
    balanced_diet = models.BooleanField(default=False)
    unbalanced_diet = models.BooleanField(default=False)
    good_sleep_quality = models.BooleanField(default=False)
    poor_sleep_quality = models.BooleanField(default=False)
    sufficient_exercise_duration = models.BooleanField(default=False)
    lack_of_exercise = models.BooleanField(default=False)
    no_anxiety = models.BooleanField(default=False)
    anxiety = models.BooleanField(default=False)
    no_medication = models.BooleanField(default=False)
    medication = models.BooleanField(default=False)
    medication_details = models.TextField(blank=True, null=True)
    no_other_physical_conditions = models.BooleanField(default=False)
    other_physical_conditions = models.BooleanField(default=False)
    other_physical_conditions_details = models.TextField(blank=True, null=True)
    replied = models.BooleanField(default=False, verbose_name='是否已回复')

    class Meta:
        db_table = 'tb_doctor_ask'
        verbose_name = '在线问诊'
        verbose_name_plural = verbose_name



class DoctorReply(models.Model):
    # 定义与前端传入数据相关的字段
    health_diagnosis = models.CharField(max_length=200, verbose_name='健康诊断')
    offline_medical_advice = models.CharField(max_length=3, choices=[('yes', '是'), ('no', '否')], verbose_name='是否建议线下就医')
    health_analysis = models.TextField(verbose_name='健康分析')

    # 定义外键字段
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, verbose_name='医生')
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, verbose_name='健康记录')

    class Meta:
        db_table = 'tb_doctor_reply'
        verbose_name = '医生回复'
        verbose_name_plural = '医生回复'