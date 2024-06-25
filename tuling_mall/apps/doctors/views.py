import re

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone

from users.models import User, Tijian
from django.http import JsonResponse
from django.views import View
from .models import DoctorInfo
from doctors.models import DoctorOrder


class DoctorList(View):
    def get(self, request):
        # 获取所有医生记录
        doctor_records = DoctorInfo.objects.all()

        # 创建一个空的列表
        doctor_records_list = []

        # 对当前查询的结果集进行遍历
        for record in doctor_records:
            # 创建一个字典，包含医生的名字和图片 URL
            doctor_dict = dict(
                name=record.doctorname,
                doctor_image=record.doctor_image.url,
            )
            doctor_records_list.append(doctor_dict)

        # 返回 JSON 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'records': doctor_records_list})


class DoctorOrderShow(View):
    def get(self, request, doctor_id):
        doctor = DoctorInfo.objects.get(id=doctor_id)
        doctor_id=doctor_id
        doctorname = doctor.doctorname
        department = doctor.which_department.department_name
        doctorintroducation = doctor.introducation
        department_area = doctor.which_department.department_area
        doctor_image = doctor.doctor_image
        doctor_title = doctor.doctor_title
        username = request.COOKIES.get('username')

        consultation_fee = determine_consultation_fee(doctor_title)

        context = {
            'doctor_id':doctor_id,
            'doctorname': doctorname,
            'department': department,
            'doctorintroducation': doctorintroducation,
            'department_area': department_area,
            'doctor_image': doctor_image,
            'username': username,
            'doctor_title': doctor_title,
            'consultation_fee': consultation_fee
        }
        return render(request, 'doctor_order.html', context)

def determine_consultation_fee(doctor_title):
    # 根据医生职称确定咨询费用
    if doctor_title == '住院医师':
        return '30'
    elif doctor_title == '主治医师':
        return '50'
    elif doctor_title == '副主任医师':
        return '70'
    elif doctor_title == '主任医师':
        return '100'
    else:
        return '0'  # 如果医生职称未知，默认费用为0

def user_order_doctor(request):
    if request.method == "POST":
        ordertime = request.POST.get('ordertime')

        referer = request.META.get('HTTP_REFERER')
        print('Referer:', referer)
        match = re.search(r'/doctor_order/(\d+)', referer)
        doctor_id = match.group(1)

        # 获取医生信息
        doctor = DoctorInfo.objects.get(id=doctor_id)
        doctor_title = doctor.doctor_title

        # 根据医生职称确定咨询费用
        consultation_fee = determine_consultation_fee(doctor_title)

        print(consultation_fee)

        order = DoctorOrder.objects.filter(ordertime=ordertime, doctorname_id=doctor_id)
        if order:
            info = '400'
            print(info)
            return JsonResponse({"info": info})
        else:
            username = request.COOKIES.get('username')
            user = get_object_or_404(User, username=username)

            Disease = request.POST.get('Disease')
            mobile = request.POST.get('mobile')

            # 获取用户的过敏史和家族遗传病史
            allergy = '有' if user.allergy_history == '1' else '无'
            family_history = '有' if user.family_genetic_disease_history == '1' else '无'

            diet_habits = request.POST.get('dietHabits')
            exercise_habits = request.POST.get('exerciseHabits')
            stay_up_late = request.POST.get('stayUpLate')

            print(allergy)
            print(family_history)
            print(diet_habits)
            print(exercise_habits)
            print(stay_up_late)

            DoctorOrder.objects.create(username=user, doctorname_id=doctor_id, ordertime=ordertime, ordertip=Disease,
                                        allergy=allergy, familyHistory=family_history, mobile_phone=mobile,diet_habits=diet_habits,
                                       exercise_habits=exercise_habits,stay_up_late=stay_up_late,consultation_fee=consultation_fee)




    return JsonResponse({'code':0})




def check_appointment(request):
    doctorname = request.GET.get('doctorname')
    ordertime=request.GET.get('ordertime')
    print(ordertime)

    # 检查是否有重复的预约
    order_exists = DoctorOrder.objects.filter(ordertime=ordertime, doctorname=doctorname).exists()

    return JsonResponse({'is_full': order_exists})



def success_page(request):
    return render(request, 'DO_success.html')


from django.views import View
from django.http import JsonResponse
import re
from doctors.models import DoctorInfo
import json
class DoctorLogin(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            # 查询数据库中是否存在匹配的用户
            user = DoctorInfo.objects.get(username=username)
        except DoctorInfo.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 直接比较密码
        if user.password != password:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 成功匹配，登录用户
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', username, max_age=3600 * 24 * 15)
        return response


from medicine.models import SKU, SPU, GoodsCategory


def doctor_medicine_list(request):
    medicine_list=SKU.objects.all()
    paginator = Paginator(medicine_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor_medicine_list.html', {"page_obj":page_obj})


def doctor_edit_medicine(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        sku = SKU.objects.get(id=id)

        # 更新 SKU 字段
        sku.name = request.POST.get('name')
        sku.caption = request.POST.get('caption')
        sku.spu_id = request.POST.get('spu')
        sku.category_id = request.POST.get('category')
        sku.price = request.POST.get('price')
        sku.cost_price = request.POST.get('cost_price')
        sku.market_price = request.POST.get('market_price')
        sku.stock = request.POST.get('stock')
        sku.sales = request.POST.get('sales')
        sku.comments = request.POST.get('comments')
        sku.is_launched = 'is_launched' in request.POST
        sku.default_image = request.FILES.get('default_image')

        sku.save()
        return redirect('/doctor_medicine_list/')
    else:
        id = request.GET.get('id')
        sku = SKU.objects.get(id=id)
        return render(request, 'doctor_edit_medicine.html', {'sku': sku})

def doctor_add_medicine(request):
    spus = SPU.objects.all()
    categories = GoodsCategory.objects.all()
    if request.method == "POST":
        # medicine_name= request.POST.get('medicine_name')
        # cost_price = request.POST.get('cost_price')
        # market_price = request.POST.get('market_price')
        # stock = request.POST.get('stock')
        # sales = request.POST.get('sales')
        #
        #
        #
        # SKU.objects.create(name=medicine_name,cost_price=cost_price,market_price=market_price,stock=stock,sales=sales)
        return redirect('/medicine_list/')
    return render(request, "doctor_add_medicine.html", {"spus": spus, "categories": categories})
from doctors.models import DoctorOrder
from django.shortcuts import get_object_or_404


from article.models import article
def article_list(request):
    doctor_username = request.COOKIES.get('username')
    doctor_info = get_object_or_404(DoctorInfo, username=doctor_username)
    article_list=article.objects.filter(doctor_id=doctor_info.id).order_by('release_data')
    paginator = Paginator(article_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor_article.html', {"page_obj":page_obj})

from doctors.models import DoctorInfo
from article.models import Article_category



def doctor_order_list(request):
    doctor_username = request.COOKIES.get('username')

    # 根据医生用户名获取医生信息
    doctor_info = get_object_or_404(DoctorInfo, username=doctor_username)

    # 使用医生信息中的id查询医生的订单列表
    order_list = DoctorOrder.objects.filter(doctorname_id=doctor_info.id).order_by('-ordertime')
    paginator = Paginator(order_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor_order_list.html', {"page_obj": page_obj})


def doctor_info(request):
    doctor_username = request.COOKIES.get('username')

    # 根据医生用户名获取医生信息
    doctor_info = get_object_or_404(DoctorInfo, username=doctor_username)
    return render(request,'doctor_info.html',{"doctor_info": doctor_info})



def doctor_add_article(request):
    categories = Article_category.objects.all()  # 获取所有的文章类别
    if request.method=='POST':
        doctor_username = request.COOKIES.get('username')
        doctor_id = get_object_or_404(DoctorInfo, username=doctor_username).id
        doctor = DoctorInfo.objects.get(pk=doctor_id)

        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category_id')
        category = Article_category.objects.get(pk=category_id)
        introd = request.POST.get('introd')
        print(doctor,title,content,category,introd)
        article.objects.create(
            title=title,
            category=category,
            doctor=doctor,
            introd=introd,
            content=content,
            release_data=timezone.now()
        )

        return redirect('/doctor_article/')
    return render(request,'D_add_article.html',{"categories":categories})

def doctor_edit_article(request):
    categories = Article_category.objects.all()  # 获取所有的文章类别
    doctors = DoctorInfo.objects.all()
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        doctor_id = request.POST.get('doctor')
        content = request.POST.get('content')

        # 获取用户提交的类别 ID
        category_id = request.POST.get('category_id')

        # 通过医生 ID 获取相应的 DoctorInfo 实例
        doctor = DoctorInfo.objects.get(pk=doctor_id)

        # 通过类别 ID 获取相应的 Article_category 实例
        category = Article_category.objects.get(pk=category_id)

        introd = request.POST.get('introd')

        article_obj = article.objects.get(id=id)

        article_obj.title = title
        article_obj.category = category
        article_obj.doctor = doctor
        article_obj.introd = introd
        article_obj.content = content

        article_obj.save()
        return redirect('/article_list/')

    else:
        id = request.GET.get('id')
        article_obj = article.objects.get(id=id)

        return render(request, 'doctor_edit_article.html',
                      {'article_obj': article_obj, 'categories': categories, "doctors": doctors})

def doctor_tijian_list(request):
    tijian_list = Tijian.objects.all()
    paginator = Paginator(tijian_list, 10)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor_tijian_list.html', {"page_obj": page_obj})

def doctor_edit_tijian(request):
    if request.method=='POST':
        id=request.POST.get('id')
        user_id=request.POST.get('user_id')
        tijian_Data=request.POST.get('tijian_Data')
        height = request.POST.get('height')
        weight=request.POST.get('weight')
        lefteye=request.POST.get('lefteye')
        righteye=request.POST.get('righteye')

        tijian_obj = Tijian.objects.get(id=id)

        tijian_obj.user_id=user_id
        tijian_obj.tijian_Data=tijian_Data
        tijian_obj.height=height
        tijian_obj.weight=weight
        tijian_obj.lefteye=lefteye
        tijian_obj.righteye=righteye
        tijian_obj.save()
        return redirect('/doctor_tijian_list/')

    else:
        id=request.GET.get('id')
        tijian_obj=Tijian.objects.get(id=id)
        tijian_obj_list=Tijian.objects.all()
        return render(request, 'doctor_edit_tijian.html', {'tijian_obj':tijian_obj,"tijian_obj_list": tijian_obj_list})

def doctor_add_tijian(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        tijian_Data = request.POST.get('tijian_Data')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        lefteye = request.POST.get('lefteye')
        righteye = request.POST.get('righteye')
        blood_oxygen=request.POST.get('blood_oxygen')
        blood_pressure=request.POST.get('blood_pressure')
        heart_rate=request.POST.get('heart_rate')

        Tijian.objects.create(user_id=user_id,tijian_Data=tijian_Data,height=height,weight=weight,lefteye=lefteye,righteye=righteye,
                              blood_oxygen=blood_oxygen,blood_pressure=blood_pressure,heart_rate=heart_rate)
        return redirect('/tijian_list/')
    return render(request, "doctor_add_tijian.html")


class department_choice(View):
    def post(self,request):
        data = json.loads(request.body)
        department_id = data.get('department_id')
        print(department_id)
        doctors = DoctorInfo.objects.filter(which_department_id=department_id)
        doctors_records_list=[]
        for record in doctors:
            doctor_dict=dict(
                id=record.id,
                doctor_name=record.doctorname,
                doctor_image=record.doctor_image.url if record.doctor_image else None,
                doctor_title=record.doctor_title
            )
            doctors_records_list.append(doctor_dict)


        return JsonResponse({'code': 0,'records':doctors_records_list})

from datetime import datetime
from doctors.models import HealthRecord
class DoctorAsk(View):
    def post(self, request):
        # 获取POST请求中的表单数据
        try:
            form_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        username = form_data.get('username')
        user_instance = User.objects.get(username=username)
        doctor_instance = DoctorInfo.objects.get(id=1)
        current_time = datetime.now()
        blood_pressure = form_data.get('bloodPressure', '')
        body_temperature = form_data.get('bodyTemperature', '')
        heart_rate = form_data.get('heartRate', '')
        blood_sugar = form_data.get('bloodSugar', '')
        body_weight = form_data.get('bodyWeight', '')
        body_height = form_data.get('bodyHeight', '')
        blood_oxygen = form_data.get('bloodOxygen', '')
        # 身体状况
        no_symptoms = form_data.get('noSymptoms', False)
        headache = form_data.get('headache', False)
        fever = form_data.get('fever', False)
        cough = form_data.get('cough', False)
        chest_pain = form_data.get('chestPain', False)
        abdominal_pain = form_data.get('abdominalPain', False)
        nausea = form_data.get('nausea', False)
        vomiting = form_data.get('vomiting', False)
        other_symptoms = form_data.get('otherSymptoms', '')


        # 其他身体状况
        balanced_diet = form_data.get('balancedDiet', False)
        unbalanced_diet = form_data.get('unbalancedDiet', False)
        good_sleep_quality = form_data.get('goodSleepQuality', False)
        poor_sleep_quality = form_data.get('poorSleepQuality', False)
        sufficient_exercise_duration = form_data.get('sufficientExerciseDuration', False)
        lack_of_exercise = form_data.get('lackOfExercise', False)
        no_anxiety = form_data.get('noAnxiety', False)
        anxiety = form_data.get('anxiety', False)
        no_medication = form_data.get('noMedication', False)
        medication = form_data.get('medication', False)
        medication_details = form_data.get('medicationDetails', '')
        no_other_physical_conditions = form_data.get('noOtherPhysicalConditions', False)
        other_physical_conditions = form_data.get('otherPhysicalConditions', False)
        other_physical_conditions_details = form_data.get('otherPhysicalConditionsDetails', '')

        health_record = HealthRecord.objects.create(
            current_time=current_time,
            username=user_instance,
            doctorname=doctor_instance,
            blood_pressure=blood_pressure,
            body_temperature=body_temperature,
            heart_rate=heart_rate,
            blood_sugar=blood_sugar,
            body_weight=body_weight,
            body_height=body_height,
            blood_oxygen=blood_oxygen,
            no_symptoms=no_symptoms,
            headache=headache,
            fever=fever,
            cough=cough,
            chest_pain=chest_pain,
            abdominal_pain=abdominal_pain,
            nausea=nausea,
            vomiting=vomiting,
            other_symptoms=other_symptoms,
            balanced_diet=balanced_diet,
            unbalanced_diet=unbalanced_diet,
            good_sleep_quality=good_sleep_quality,
            poor_sleep_quality=poor_sleep_quality,
            sufficient_exercise_duration=sufficient_exercise_duration,
            lack_of_exercise=lack_of_exercise,
            no_anxiety=no_anxiety,
            anxiety=anxiety,
            no_medication=no_medication,
            medication=medication,
            medication_details=medication_details,
            no_other_physical_conditions=no_other_physical_conditions,
            other_physical_conditions=other_physical_conditions,
            other_physical_conditions_details=other_physical_conditions_details
        )



        # 返回JSON响应
        return JsonResponse({'message': 'Data received successfully.'})

def doctor_index(request):

    return render(request,'doctor_index.html')

from doctors.models import HealthRecord


def online_ask(request):
    ask = HealthRecord.objects.filter(doctorname=1, replied=False)


    return render(request, 'online_ask.html', {'ask': ask})


def record_detail(request, record_id):
    record = get_object_or_404(HealthRecord, pk=record_id)
    return render(request, 'record_detail.html', {'record': record})


from doctors.models import DoctorReply
def handle_form_submission(request):
    if request.method == 'POST':
        # 获取POST请求中的表单数据
        data = json.loads(request.body)

        # 获取JSON数据中的各个字段
        health_diagnosis = data.get('health_diagnosis')
        offline_medical_advice = data.get('offline_medical_advice')
        health_analysis = data.get('health_analysis')
        doctor_instance = DoctorInfo.objects.get(id=1)
        health_record_id = data.get('health_record_id')
        print(health_record_id)
        health_record_instance = HealthRecord.objects.get(id=health_record_id)

        doctor_reply_instance = DoctorReply.objects.create(
            health_diagnosis=health_diagnosis,
            offline_medical_advice=offline_medical_advice,
            health_analysis=health_analysis,
            doctor=doctor_instance,
            health_record=health_record_instance
        )

        health_record_instance.replied = True
        health_record_instance.save()
        print(health_record_instance)
        # 返回 JSON 响应
        return JsonResponse({'status': 'success', 'message': 'Form data received successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'})


