from datetime import datetime

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import re
from .models import User
import json
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .models import Tijian
from.models import Address


# Create your views here.

class UsernameCountView(View):
    def get(self, request, username):
        # 1. 接收用户名，并检验用户名合法性


        # 2. 根据用户名进行数据库查询
        count = User.objects.filter(username=username).count()

        # 3. 将查询结果返回给前端
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


'''
注册功能
    前端
        用户输入用户名 密码 确认密码 手机号 是否同意协议
        如果当前的值都没有问题，并且用户点击了注册按钮
        前端就会发送一个请求

    后端
        请求：接收请求，获取数据
        业务逻辑：验证数据，数据入库
        响应：{'code': 0, 'errmsg': 'ok'}

    路由：
        POST register/

    步骤：
        1. 接收请求
        2. 获取数据
        3. 验证数据
            1. 用户名 密码 确认密码 手机号 协议 等参数
            2. 用户名必须满足要求， 并不能重复
            3. 密码满足规则
            4. 确认密码必须与之前填写的密码一致
            5. 手机号满足规则 不能重复
            6. 必须同意协议
        4. 数据入库
        5. 返回响应
    '''


class RegisterView(View):
    def post(self, request):

        body_bytes = request.body

        body_dict = json.loads(body_bytes)

        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')

        allow = body_dict.get('allow')
        # 3. 数据验证
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数'})
        #   2. 用户名满足规则
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})

        #     3. 密码满足规则
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        #     4. 确认密码必须与之前输入的密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        #     5. 手机号满足规则，并不能重复
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})

        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
        try:
            user = User(username=username, mobile=mobile)
            user.set_password(password)
            user.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})


        login(request,user)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})



class LoginView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembeded')

        if not all(['username','password']):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        if re.match(r'1[3-9]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'

        user=authenticate(username=username,password=password)
        print(user)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        login(request,user)
        response=JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('username',username,max_age=3600*24*15)
        return response

class LogoutView(View):
    def delete(self,request):
        logout(request)

        response=JsonResponse({'code':400,'errmsg':'ok'})
        response.delete_cookie('username')

        return response



# class LoginRequiredJSONMixin_2(LoginRequiredMixin):
#     def handle_no_permission(self):
#         return JsonResponse({'code': 400, 'errmsg': '账号未登录'})


from utils.views import LoginRequiredJSONMixin


class CenterView(LoginRequiredJSONMixin, View):
    def get(self, request):
        allergy_history = "无" if request.user.allergy_history == "0" else "有"
        family_genetic_disease_history = "无" if request.user.family_genetic_disease_history == "0" else "有"

        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
            'allergy_history': allergy_history,
            'family_genetic_disease_history': family_genetic_disease_history
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})

class edit_info(LoginRequiredJSONMixin,View):
    def post(self, request):
        user = request.user
        # 解析请求体中的JSON数据
        data = json.loads(request.body.decode('utf-8'))

        # 获取家族遗传病史和过敏史的值
        family_history = data.get('familyHistory')
        allergy_history = data.get('allergyHistory')

        # 更新用户的过敏史和家族遗传病史
        if family_history is not None:
            user.family_genetic_disease_history = family_history
        if allergy_history is not None:
            user.allergy_history = allergy_history

        # 保存用户信息到数据库
        user.save()

        # 返回一个JSON响应
        return JsonResponse({"msg": "success"})

class ShowTijianRecords(LoginRequiredJSONMixin,View):
    def get(self, request):
        # 1. 获取当前登录用户的所有体检记录
        tijian_records = Tijian.objects.filter(user=request.user)



        # 2. 创建一个空的列表
        tijian_records_list = []
        real_name = request.user.real_name
        username=request.user.username
        # 3. 对当前查询的结果集进行遍历
        for record in tijian_records:


            # 创建一个字典
            tijian_dict = dict(
                id=record.id,
                tijian_Date=record.tijian_Data,
                height=record.height,
                weight=record.weight,
                lefteye=record.lefteye,
                righteye=record.righteye,
                blood_pressure=record.blood_pressure,
                heart_rate=record.heart_rate,
                blood_oxygen=record.blood_oxygen,
                username=real_name


            )
            tijian_records_list.append(tijian_dict)
            print(tijian_records_list)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'records': tijian_records_list,'username':username})




class AddressCreateView(LoginRequiredJSONMixin,View):
    def post(self,request):
        user=request.user
        data=json.loads(request.body)

        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        # 4. 验证参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile错误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})

        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})


            try:
                address = Address.objects.create(
                        # 外键 需要保存用户实例对象 而不是一个具体的值
                        user=user,
                        title=receiver,
                        receiver=receiver,
                        province_id=province_id,
                        city_id=city_id,
                        district_id=district_id,
                        place=place,
                        mobile=mobile,
                        tel=tel,
                        email=email
                    )
            except Exception as e:
                print(e)
                return JsonResponse({'code': 400, 'errmsg': '数据库入库出错'})


            address_dict = {
            'id': address.id,
            'title': address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }


            return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


class ShowAddress(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1. 获取当前登录用户的所有地址
        addresses = Address.objects.filter(user=request.user, is_deleted=False)

        # 2. 创建一个空的列表
        address_dict_list = []

        # 3. 对当前查询的结果集进行遍历
        for address in addresses:
            # 创建一个字典
            address_dict = dict(
                id=address.id,
                title=address.title,
                receiver=address.receiver,
                province=address.province.name,
                city=address.city.name,
                district=address.district.name,
                place=address.place,
                mobile=address.mobile,
                tel=address.tel,
                email=address.email
            )
            address_dict_list.append(address_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_dict_list})


# 数据更新
class UpdateAddressView(LoginRequiredJSONMixin, View):
    def put(self, request, address_id):
        # 1. 接收参数
        json_dict = json.loads(request.body)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验地址
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile错误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})

        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})

        # 在修改前 需要判断当前地址是否存在
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )

        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '更新地址失败'})

        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = dict(
            id=address.id,
            title=address.title,
            receiver=address.receiver,
            province=address.province.name,
            city=address.city.name,
            district=address.district.name,
            place=address.place,
            mobile=address.mobile,
            tel=address.tel,
            email=address.email

        )

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})

    def delete(self, request, address_id):
        # 1. 查询需要删除的地址
        try:
            address = Address.objects.get(id=address_id)

            # 2. 进行逻辑删除并保存当前删除状态
            address.is_deleted = True
            address.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '删除地址失败'})

        # 3. 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class ChangePassWordView(LoginRequiredJSONMixin, View):
    def put(self, request):
        # 1. 接收请求 获取参数
        dict_data = json.loads(request.body)
        old_password = dict_data.get('old_password')
        new_password = dict_data.get('new_password')
        new_password2 = dict_data.get('new_password2')

        # 2. 校验参数
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数'})

        # 前端传过来的密码没有加密 所以后端接收到旧密码之后需要进行解密操作
        # 从数据库拿出密码并进行解密
        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({'code': 400, 'errmsg': '原始密码不正确'})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400, 'errmsg': '密码最少8位, 最长20位'})

        if new_password != new_password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入密码不一致'})

        # 3. 修改密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '修改密码失败'})

        # 4. 清除登录状态 session 信息
        logout(request)

        # 5. 构造响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        # 删除 cookie 信息
        response.delete_cookie('username')

        # 6. 返回响应
        return response




from orders.models import OrderInfo,OrderGoods

from django.http import JsonResponse

class ShowOrderRecords(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1. 获取当前登录用户的所有订单记录
        order_records = OrderInfo.objects.filter(user=request.user)

        # 2. 创建一个空的列表
        order_records_list = []

        # 3. 对当前查询的结果集进行遍历
        for record in order_records:
            # 获取与订单关联的商品记录
            order_goods = OrderGoods.objects.filter(order=record)
            status_map = {
                1: "待支付",
                2: "待发货",
                3: "待收货",
                4: "待评价",
                5: "已完成",
                6: "已取消"
            }
            status_cn = status_map.get(record.status, "未知状态")

            # 创建一个字典
            order_dict = dict(
                order_id=record.order_id,
                total_count=record.total_count,
                total_amount=record.total_amount,
                freight=record.freight,
                order_goods=[],
                status=status_cn

            )

            # 遍历关联的订单商品记录
            for goods in order_goods:
                # 将订单商品信息添加到字典中
                order_goods_dict = dict(
                    sku_name=goods.sku.name,
                    count=goods.count,
                    price=goods.price,
                    comment=goods.comment,
                    score=goods.score,
                    is_anonymous=goods.is_anonymous,
                    is_commented=goods.is_commented,
                    default_image=str(goods.sku.default_image)
                )
                order_dict['order_goods'].append(order_goods_dict)

            # 将订单字典添加到列表中
            order_records_list.append(order_dict)

        # 4. 返回JSON响应

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'records': order_records_list})


from doctors.models import DoctorOrder
class ShowDoctorOrderRecords(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1. 获取当前登录用户的所有体检记录
        doctor_order_records = DoctorOrder.objects.filter(username=request.user,is_verified=True)

        # 2. 创建一个空的列表
        doctor_order_records_list = []

        # 3. 对当前查询的结果集进行遍历
        for record in doctor_order_records:
            # 获取医生姓名
            doctor_name = record.doctorname.doctorname if record.doctorname else ''
            department_name = record.doctorname.which_department.department_name if record.doctorname and record.doctorname.which_department else ''
            department_area = record.doctorname.which_department.department_area if record.doctorname and record.doctorname.which_department else ''

            # 创建一个字典
            doctor_order_dict = dict(
                id=record.id,
                ordertime=record.ordertime,
                ordertip=record.ordertip,
                doctor_name=doctor_name,
                allegry=record.allergy,
                familyHistory=record.familyHistory,

                department_name=department_name,
                department_area=department_area
            )
            doctor_order_records_list.append(doctor_order_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'records': doctor_order_records_list})

class TijianOrderShow(View):
    def get(self,request):
        username = request.COOKIES.get('username')
        context = {
            'username' :username
        }

        return render(request,'tijian_order.html',context)

from .models import TijianOrder
# def user_order_tijian(request):
#     if request.method == "POST":
#         ordertime = request.POST.get('ordertime')
#         order = TijianOrder.objects.filter(ordertime=ordertime)
#         if order:
#             info = '400'
#             print(info)
#             return JsonResponse({"info": info})
#         else:
#             username=request.COOKIES.get('username')
#             user_id=User.objects.get(username=username).id
#
#             checkupType = request.POST.get('checkupType')
#
#             Disease = request.POST.get('Disease')
#             allergy = request.POST.get('allergy')
#             family_history = request.POST.get('familyHistory')
#
#             TijianOrder.objects.create(username_id=user_id,checkupTypee=checkupType,ordertime=ordertime,ordertip=Disease,allergy=allergy,
#                 familyHistory=family_history)
#
#     return JsonResponse({'code':0})
def check_tj_appointment(request):
    selected_date = request.GET.get('selectedDate')
    selected_time = request.GET.get('selectedTime')

    # 将传入的日期和时间字符串转换为datetime对象
    selected_datetime = datetime.strptime(selected_date + " " + selected_time, "%m/%d/%Y %H:%M")

    # 将日期和时间对象转换为数据库中存储的格式
    formatted_date = selected_datetime.strftime("%Y-%m-%d")
    formatted_time = selected_datetime.strftime("%H:%M")

    # 检查是否有重复的预约
    appointment_exists = TijianOrder.objects.filter(orderDate=formatted_date, orderTime=formatted_time).exists()
    if appointment_exists:
        print('yes')
    else:
        print('no')
    return JsonResponse({'is_full': appointment_exists})



class ShowTijianOrderRecords(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1. 获取当前登录用户的所有体检预约记录
        tijian_order_records = TijianOrder.objects.filter(username=request.user, is_verified=True)

        # 2. 创建一个空的列表
        tijian_order_records_list = []

        # 3. 对当前查询的结果集进行遍历
        for record in tijian_order_records:
            # 创建一个字典，映射数据库字段到前端需要的字段名
            tijian_order_dict = {
                'id': record.id,
                'orderdate': record.orderDate,
                'ordertime': record.orderTime,
                'ordertip': record.ordertip,
                'checkupType': record.checkupType,
                'allergy': record.allergy,
                'familyHistory': record.familyHistory,
                'additionalInfo': record.additionalInfo,
                'xRay': record.xRay,
                'bloodTest': record.bloodTest,
                'urineTest': record.urineTest,
                'totalPrice': record.totalPrice,
                'institution': record.institution
                # 如果需要其他字段，请按照类似的方式添加
            }
            tijian_order_records_list.append(tijian_order_dict)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'records': tijian_order_records_list})

from django.db.models import Avg

class ShowTijianAvg(LoginRequiredJSONMixin, View):
    def get(self, request):

        tijian_records = Tijian.objects.filter(user=request.user)

        try:
            avg_height = round(tijian_records.aggregate(Avg('height'))['height__avg'], 2)
            avg_weight = round(tijian_records.aggregate(Avg('weight'))['weight__avg'], 2)
            avg_lefteye = round(tijian_records.aggregate(Avg('lefteye'))['lefteye__avg'], 2)
            avg_righteye = round(tijian_records.aggregate(Avg('righteye'))['righteye__avg'], 2)
            avg_blood_pressure = round(tijian_records.aggregate(Avg('blood_pressure'))['blood_pressure__avg'], 2)
            avg_heart_rate = round(tijian_records.aggregate(Avg('heart_rate'))['heart_rate__avg'], 2)
            avg_blood_oxygen = round(tijian_records.aggregate(Avg('blood_oxygen'))['blood_oxygen__avg'], 2)
        except TypeError:
            avg_height = avg_weight = avg_lefteye = avg_righteye = avg_blood_pressure = avg_heart_rate = avg_blood_oxygen = 404

        response_data = {
            'code': 0,
            'errmsg': 'ok',
            'username': request.user.username,
            'average_height': avg_height,
            'average_weight': avg_weight,
            'average_lefteye': avg_lefteye,
            'average_righteye': avg_righteye,
            'average_blood_pressure': avg_blood_pressure,
            'average_heart_rate': avg_heart_rate,
            'average_blood_oxygen': avg_blood_oxygen,
        }
        print(response_data)
        return JsonResponse(response_data)
from django.core import serializers

from doctors.models import HealthRecord
def my_ask(request):
    # 获取所有健康记录
    username = request.GET.get('username')

    # 根据用户名获取用户对象
    user = User.objects.get(username=username)

    # 使用用户对象过滤健康记录
    health_records = HealthRecord.objects.filter(username=user)

    # 创建一个空的列表，用于存储处理后的记录数据
    records_list = []

    # 遍历每条健康记录，并将所需字段添加到列表中
    for record in health_records:
        # 将医生名称字段转换为字符串，以避免序列化问题
        doctor_name = record.doctorname.doctorname if record.doctorname else ""

        # 构建包含所需字段的字典
        record_data = {
            'id':record.id,
            'current_time': record.current_time,
            'doctorname': doctor_name,
            'replied': record.replied
        }
        # 将字典添加到列表中
        records_list.append(record_data)

    # 返回 JSON 响应
    return JsonResponse({'msg': 'success', 'records': records_list})

from doctors.models import DoctorReply
class DoctorReplyDetailView(View):
    def get(self, request, record_id):

        try:
            # 查询医生回复信息

            doctor_reply = DoctorReply.objects.get(health_record_id=record_id)
            # 构建医生回复的数据字典
            doctor_reply_data = {
                'health_diagnosis': doctor_reply.health_diagnosis,
                'offline_medical_advice': doctor_reply.offline_medical_advice,
                'health_analysis': doctor_reply.health_analysis
            }
            health_record = HealthRecord.objects.get(id=record_id)
            # 构建健康记录的数据字典
            health_record_data = {
                'current_time':health_record.current_time,
                'blood_pressure': health_record.blood_pressure,
                'body_temperature': health_record.body_temperature,
                'heart_rate': health_record.heart_rate,
                'blood_sugar': health_record.blood_sugar,
                'body_weight': health_record.body_weight,
                'body_height': health_record.body_height,
                'blood_oxygen': health_record.blood_oxygen,
                'no_symptoms': health_record.no_symptoms,
                'headache': health_record.headache,
                'fever': health_record.fever,
                'cough': health_record.cough,
                'chest_pain': health_record.chest_pain,
                'abdominal_pain': health_record.abdominal_pain,
                'nausea': health_record.nausea,
                'vomiting': health_record.vomiting,
                'other_symptoms': health_record.other_symptoms,
                'balanced_diet': health_record.balanced_diet,
                'unbalanced_diet': health_record.unbalanced_diet,
                'good_sleep_quality': health_record.good_sleep_quality,
                'poor_sleep_quality': health_record.poor_sleep_quality,
                'sufficient_exercise_duration': health_record.sufficient_exercise_duration,
                'lack_of_exercise': health_record.lack_of_exercise,
                'no_anxiety': health_record.no_anxiety,
                'anxiety': health_record.anxiety,
                'no_medication': health_record.no_medication,
                'medication': health_record.medication,
                'medication_details': health_record.medication_details,
                'no_other_physical_conditions': health_record.no_other_physical_conditions,
                'other_physical_conditions': health_record.other_physical_conditions,
                'other_physical_conditions_details': health_record.other_physical_conditions_details,
                'replied': health_record.replied
            }

            return JsonResponse({'doctor_reply': doctor_reply_data,'health_record': health_record_data})
        except DoctorReply.DoesNotExist:
            return JsonResponse({'error': 'Doctor reply not found'}, status=404)
