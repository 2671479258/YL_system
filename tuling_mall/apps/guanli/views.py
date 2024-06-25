from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from users.models import Tijian,User
from doctors.models import DoctorInfo,Department
from medicine.models import SKU
# Create your views here.
def add_tijian(request):
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
    return render(request, "add_tijian.html")

def tijian_list(request):
    tijian_list=Tijian.objects.all()
    paginator = Paginator(tijian_list, 10)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tijian_list.html', {"page_obj":page_obj})

def edit_tijian(request):
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
        return redirect('/tijian_list/')

    else:
        id=request.GET.get('id')
        tijian_obj=Tijian.objects.get(id=id)
        tijian_obj_list=Tijian.objects.all()
        return render(request, 'edit_tijian.html', {'tijian_obj':tijian_obj,"tijian_obj_list": tijian_obj_list})

def delete_tijian(request):
    id=request.GET.get('id')
    Tijian.objects.filter(id=id).delete()
    return redirect("/tijian_list")



def user_list(request):
    user_list=User.objects.all()
    paginator = Paginator(user_list, 10)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'user_list.html',{"page_obj": page_obj})


def add_user(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        real_name = request.POST.get('real_name')


        User.objects.create(username=username,password=password,mobile=mobile,real_name=real_name)
        return redirect('/user_list/')
    return render(request, "add_user.html")


def edit_user(request):
    if request.method=='POST':
        id=request.POST.get('id')
        username=request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        real_name = request.POST.get('real_name')
        user_obj = User.objects.get(id=id)
        user_obj.username=username
        user_obj.password=password
        user_obj.mobile=mobile
        user_obj.real_name=real_name

        user_obj.save()
        return redirect('/user_list/')

    else:
        id=request.GET.get('id')
        user_obj=User.objects.get(id=id)
        user_obj_list=User.objects.all()
        return render(request, 'edit_user.html', {'user_obj':user_obj,"user_obj_list": user_obj_list})

def delete_user(request):
    id=request.GET.get('id')
    User.objects.filter(id=id).delete()
    return redirect("/user_list")

def search_user(request):
    if request.method == 'POST':
        name = request.POST.get('search_user_name')
        users_search_list = User.objects.filter(real_name__contains=name).all()
        return render(request, 'search_user_name.html', {'user_search_list': users_search_list})
    else:
        return render(request, 'search_user_name.html', {})

def department_list(request):
    department_list=Department.objects.all()
    paginator = Paginator(department_list, 8)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'department_list.html',{"page_obj":page_obj})

def add_department(request):
    if request.method == "POST":

        department_name = request.POST.get('department_name')
        department_area = request.POST.get('department_area')
        department_introduce = request.POST.get('department_introduce')



        Department.objects.create(department_name=department_name,department_area=department_area,department_introduce=department_introduce)
        return redirect('/department_list/')
    return render(request, "add_department.html")

def edit_department(request):
    if request.method=='POST':
        id=request.POST.get('id')
        department_name=request.POST.get('department_name')
        department_area = request.POST.get('department_area')
        department_introduce = request.POST.get('department_introduce')



        department_obj = Department.objects.get(id=id)

        department_obj.department_name=department_name
        department_obj.department_area=department_area
        department_obj.department_introduce=department_introduce


        department_obj.save()
        return redirect('/department_list/')

    else:
        id=request.GET.get('id')
        department_obj=Department.objects.get(id=id)
        department_obj_list=Department.objects.all()
        return render(request, 'edit_department.html', {'department_obj':department_obj,"department_obj_list": department_obj_list})

def delete_department(request):
    id=request.GET.get('id')
    Department.objects.filter(id=id).delete()
    return redirect("/department_list")

def doctor_list(request):
    doctor_list = DoctorInfo.objects.all()
    paginator = Paginator(doctor_list, 10)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor_list.html', {"page_obj": page_obj})

def add_doctor(request):
    departments = Department.objects.all()
    if request.method == "POST":

        username = request.POST.get('username')
        doctorname = request.POST.get('doctorname')
        password = request.POST.get('password')
        introducation = request.POST.get('introducation')
        which_department_id = request.POST.get('which_department_id')



        DoctorInfo.objects.create(username=username,doctorname=doctorname,password=password,introducation=introducation,which_department_id=which_department_id)
        return redirect('/doctor_list/')
    return render(request, "add_doctor.html",{'departments':departments})


def edit_doctor(request):
    if request.method=='POST':
        id=request.POST.get('id')
        username=request.POST.get('username')
        doctorname= request.POST.get('doctorname')
        password = request.POST.get('password')
        introducation = request.POST.get('introducation')
        which_department_id=request.POST.get('which_department_id')


        doctor_obj = DoctorInfo.objects.get(id=id)

        doctor_obj.useranme=username
        doctor_obj.doctorname=doctorname
        doctor_obj.password=password
        doctor_obj.introducation=introducation
        doctor_obj.which_department_id=which_department_id


        doctor_obj.save()
        return redirect('/doctor_list/')

    else:
        id=request.GET.get('id')
        doctor_obj=DoctorInfo.objects.get(id=id)
        doctor_obj_list=DoctorInfo.objects.all()
        return render(request, 'edit_doctor.html', {'doctor_obj':doctor_obj,"doctor_obj_list": doctor_obj_list})


def delete_doctor(request):
    id=request.GET.get('id')
    DoctorInfo.objects.filter(id=id).delete()
    return redirect("/doctor_list")

def search_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('search_doctor_name')

        doctors_search_list = DoctorInfo.objects.filter(doctorname__contains=name).all()
        # 使用 __icontains 来进行匹配，这样可以不区分大小写地查找包含医生姓名的记录

        return render(request, 'search_doctor_name.html', {'doctors_search_list': doctors_search_list})
    else:
        # 如果不是 POST 请求，可以返回一个空的页面或者其他处理方式
        return render(request, 'search_doctor_name.html', {})

def medicine_list(request):
    medicine_list=SKU.objects.all()
    paginator = Paginator(medicine_list, 8)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'medicine_list.html', {"page_obj":page_obj})

from medicine.models import SPU,GoodsCategory
def add_medicine(request):
    spus=SPU.objects.all()
    categories=GoodsCategory.objects.all()
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
    return render(request, "add_medicine.html", {"spus":spus,"categories":categories})
#
#
def edit_medicine(request):
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
        return redirect('/medicine_list/')
    else:
        id = request.GET.get('id')
        sku = SKU.objects.get(id=id)
        return render(request, 'edit_medicine.html', {'sku': sku})
#
#
def delete_medicine(request):
    id=request.GET.get('id')
    SKU.objects.filter(id=id).delete()
    return redirect("/medicine_list")

def search_medicine(request):
    if request.method == "POST":
        name=request.POST.get('search_medicine_name')
        medicine_search_list=SKU.objects.filter(name__contains=name).all()
        return render(request, 'search_medicine_name.html', {'medicine_search_list': medicine_search_list})
    else:
        # 如果不是 POST 请求，可以返回一个空的页面或者其他处理方式
        return render(request, 'search_medicine_name.html', {})


from doctors.models import DoctorOrder
def order_list(request):
    order_list=DoctorOrder.objects.all()
    paginator = Paginator(order_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'order_list.html',{"page_obj":page_obj})

def edit_order(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        doctor_obj = DoctorOrder.objects.get(id=id)

        # Updating doctor order fields
        doctor_obj.doctorname_id = request.POST.get('doctorname')
        doctor_obj.username_id = request.POST.get('username')
        doctor_obj.ordertime = request.POST.get('ordertime')
        doctor_obj.ordertip = request.POST.get('ordertip')
        doctor_obj.allergy = request.POST.get('allergy')
        doctor_obj.familyHistory = request.POST.get('familyHistory')
        doctor_obj.mobile_phone = request.POST.get('mobile_phone')
        doctor_obj.is_verified = 'is_verified' in request.POST

        # New fields
        doctor_obj.diet_habits = request.POST.get('diet_habits')
        doctor_obj.exercise_habits = request.POST.get('exercise_habits')
        doctor_obj.stay_up_late = request.POST.get('stay_up_late')
        doctor_obj.consultation_fee = request.POST.get('consultation_fee')

        doctor_obj.save()
        return redirect('/order_list/')
    else:
        id = request.GET.get('id')
        doctor_obj = DoctorOrder.objects.get(id=id)
        return render(request, 'edit_order.html', {'doctor_obj': doctor_obj})
def add_order(request):
    if request.method == 'POST':
        doctor_id = request.POST['doctorname']
        user_id = request.POST['username']
        order_date = request.POST['orderDate']
        order_time = request.POST['orderTime']
        order_tip = request.POST['ordertip']
        allergy = request.POST['allergy']
        family_history = request.POST['familyHistory']
        mobile_phone = request.POST['mobile_phone']
        diet_habits = request.POST['diet_habits']
        exercise_habits = request.POST['exercise_habits']
        stay_up_late = request.POST['stay_up_late']
        consultation_fee = request.POST['consultation_fee']
        is_verified = 'is_verified' in request.POST
        users = User.objects.all()
        doctors = DoctorInfo.objects.all()
        # 组合预约日期和时间
        order_datetime = datetime.strptime(f"{order_date} {order_time}", "%Y-%m-%d %H:%M")
        order_datetime_str = order_datetime.strftime("%Y年%m月%d日 %H:%M")

        doctor_order = DoctorOrder(
            doctorname_id=doctor_id,
            username_id=user_id,
            ordertime=order_datetime_str,
            ordertip=order_tip,
            allergy=allergy,
            familyHistory=family_history,
            mobile_phone=mobile_phone,
            diet_habits=diet_habits,
            exercise_habits=exercise_habits,
            stay_up_late=stay_up_late,
            consultation_fee=consultation_fee,
            is_verified=is_verified
        )
        doctor_order.save()
        return redirect('success_url')  # 替换为实际的成功跳转页面

    doctors = DoctorInfo.objects.all()
    users = User.objects.all()
    return render(request, 'add_order.html', {'doctors': doctors, 'users': users})



def order_list_0(request):
    order_list=DoctorOrder.objects.filter(is_verified=False)
    paginator = Paginator(order_list, 5)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'order_list_0.html',{"page_obj":page_obj})

def pass_order_0(request):
    if request.method == 'GET' and 'id' in request.GET:
        order_id = request.GET['id']
        order = get_object_or_404(DoctorOrder, id=order_id)
        order.is_verified = True
        order.save()
        return redirect('/order_list_0/')
    else:
        # Handle other HTTP methods or requests without an ID parameter
        return redirect('/order_list_0/')  # Redirect to the list view if the request is invalid

from orders.models import OrderGoods,OrderInfo
def goods_list(request):
    goods_list=OrderGoods.objects.all()
    paginator = Paginator(goods_list, 8)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'goods_list.html',{"page_obj":page_obj})





from users.models import TijianOrder
def TjOrder_list(request):
    TjOrder_list=TijianOrder.objects.all()
    paginator = Paginator(TjOrder_list, 5)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tj_order_list.html', {"page_obj": page_obj})

def TjOrder_list_0(request):
    TjOrder_list = TijianOrder.objects.filter(is_verified=False)
    paginator = Paginator(TjOrder_list, 5)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tj_order_list_0.html', {"page_obj": page_obj})

def edit_tijian_order(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        tijian_order = TijianOrder.objects.get(id=id)

        # 更新体检预约信息字段
        tijian_order.username_id = request.POST.get('username')
        tijian_order.checkupType = request.POST.get('checkupType')
        tijian_order.orderDate = request.POST.get('orderDate')
        tijian_order.orderTime = request.POST.get('orderTime')
        tijian_order.ordertip = request.POST.get('ordertip')
        tijian_order.allergy = request.POST.get('allergy', '无')
        tijian_order.familyHistory = request.POST.get('familyHistory', '无')
        tijian_order.additionalInfo = request.POST.get('additionalInfo', '')
        tijian_order.xRay = 'xRay' in request.POST
        tijian_order.bloodTest = 'bloodTest' in request.POST
        tijian_order.urineTest = 'urineTest' in request.POST
        tijian_order.totalPrice = request.POST.get('totalPrice', 0)
        tijian_order.institution = request.POST.get('institution', '')
        tijian_order.is_verified = 'is_verified' in request.POST

        tijian_order.save()
        return redirect('/tijian_order_list/')
    else:
        id = request.GET.get('id')
        tijian_order = TijianOrder.objects.get(id=id)
        return render(request, 'edit_tijian_order.html', {'tijian_order': tijian_order})

def pass_tijian_0(request):
    if request.method == 'GET' and 'id' in request.GET:
        order_id = request.GET['id']
        order = get_object_or_404(TijianOrder, id=order_id)
        order.is_verified = True
        order.save()
        return redirect('/tj_order_list_0/')
    else:
        # Handle other HTTP methods or requests without an ID parameter
        return redirect('TjOrder_list_0')  # Redirect to the list view if the request is invalid

def add_TjOrder(request):
    users=User.objects.all()
    if request.method == "POST":



        return redirect('/tj_order_list/')
    return render(request, "add_tj_order.html",{'users':users})
from article.models import article
def Article_list(request):
    article_list=article.objects.all()
    paginator = Paginator(article_list, 5)  # 每页显示 10 个医生信息
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'article_list.html', {"page_obj": page_obj})




from article.models import Article_category
def add_article(request):
    categories = Article_category.objects.all()  # 获取所有的文章类别
    doctors=DoctorInfo.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        doctor_id = request.POST.get('doctor')
        content = request.POST.get('content')

        # 获取用户提交的类别 ID
        category_id = request.POST.get('category_id')

        # 通过医生 ID 获取相应的 DoctorInfo 实例
        doctor = DoctorInfo.objects.get(pk=doctor_id)

        # 通过类别 ID 获取相应的 Article_category 实例
        category = Article_category.objects.get(pk=category_id)

        introd=request.POST.get('introd')
        article.objects.create(
            title=title,
            category=category,
            doctor=doctor,
            introd=introd,
            content=content,
            release_data=timezone.now()
        )
        return redirect('/article_list/')
    return render(request, "add_article.html", {'categories': categories,"doctors":doctors})

def edit_article(request):
    categories = Article_category.objects.all()  # 获取所有的文章类别
    doctors = DoctorInfo.objects.all()
    if request.method=='POST':
        id=request.POST.get('id')
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

        article_obj.title=title
        article_obj.category=category
        article_obj.doctor=doctor
        article_obj.introd=introd
        article_obj.content=content


        article_obj.save()
        return redirect('/article_list/')

    else:
        id=request.GET.get('id')
        article_obj=article.objects.get(id=id)

        return render(request, 'edit_article.html', {'article_obj':article_obj,'categories': categories,"doctors":doctors})

def search_article(request):
    if request.method == 'POST':
        name = request.POST.get('search_article_name')
        article_search_list = article.objects.filter(title__contains=name).all()
        # 使用 __icontains 来进行匹配，这样可以不区分大小写地查找包含医生姓名的记录

        return render(request, 'search_article.html', {'Article_list': article_search_list})
    else:
        # 如果不是 POST 请求，可以返回一个空的页面或者其他处理方式
        return render(request, 'search_article.html', {})


def guanli_index(request):

    return render(request,'guanli_index.html')


def test(request):

    tijian_list=Tijian.objects.all()
    return render(request, 'test.html', {"tijian_obj_list":tijian_list})


