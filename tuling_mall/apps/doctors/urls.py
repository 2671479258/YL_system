from . import views
from django.urls import path
urlpatterns = [
    path('doctor_show/',views.DoctorList.as_view()),
    path('doctor_order/<doctor_id>',views.DoctorOrderShow.as_view()),
    path('user_order_doctor/', views.user_order_doctor, name='user_order_doctor'),
    path('doctor_medicine_list/',views.doctor_medicine_list),
    path('doctor_add_medicine/', views.doctor_add_medicine),
path('doctor_edit_medicine/',views.doctor_edit_medicine),

    path('doctorlogin/',views.DoctorLogin.as_view()),
path('doctor_article/',views.article_list),
path('doctor_edit_article/',views.doctor_edit_article),
path('doctor_tijian_list/',views.doctor_tijian_list),
path('doctor_edit_tijian/',views.doctor_edit_tijian),
path('doctor_add_tijian/',views.doctor_add_tijian),
path('doctor_order_list/',views.doctor_order_list),
    path('doctor_info/',views.doctor_info),
    path('doctor_add_article/',views.doctor_add_article),
    path('department_choice/',views.department_choice.as_view()),
path('DO_success/', views.success_page),
    path('doctor_ask/',views.DoctorAsk.as_view()),
path('doctor_index/',views.doctor_index),
    path('online_ask/',views.online_ask),
    path('record/<int:record_id>/', views.record_detail, name='record_detail'),
path('submit-form/', views.handle_form_submission, name='submit_form'),
    path('api/check_appointment/', views.check_appointment, name='check_appointment'),

    ]