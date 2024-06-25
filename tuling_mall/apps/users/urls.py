from . import views
from django.urls import path
from utils.converters import UsernameConverter,MobileConverter
from django.urls import register_converter

register_converter(UsernameConverter,'username')
register_converter(MobileConverter,'mobile')
urlpatterns = [
    path('usernames/<username:username>/count/',views.UsernameCountView.as_view()),
    path('mobile/<mobile:mobile>/count/',views.MobileCountView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('info/',views.CenterView.as_view()),
    path('edit_info/', views.edit_info.as_view()),
    path('tijian/', views.ShowTijianRecords.as_view()),
    path('addresses/create/',views.AddressCreateView.as_view()),
    path('addresses/',views.ShowAddress.as_view()),
    path('addresses/<address_id>/',views.UpdateAddressView.as_view()),
    path('password/',views.ChangePassWordView.as_view()),
    path('userorder/',views.ShowOrderRecords.as_view()),
    path('show_doctor_order/',views.ShowDoctorOrderRecords.as_view()),
    path('tijian_order/',views.TijianOrderShow.as_view()),
    # path('user_order_tijian/',views.user_order_tijian,name='user_order_tijian'),
    path('api/check_tj_appointment/', views.check_tj_appointment, name='check_tj_appointment'),

    path('show_tijian_order/',views.ShowTijianOrderRecords.as_view()),
    path('show_tijian_avg/', views.ShowTijianAvg.as_view()),
    path('my_ask/',views.my_ask),
path('view_doctor_reply/<int:record_id>/', views.DoctorReplyDetailView.as_view(), name='view_doctor_reply'),

]
