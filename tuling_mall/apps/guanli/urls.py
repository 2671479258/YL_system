from django.urls import path
from guanli import views
urlpatterns = [
    path('add_tijian/', views.add_tijian),
    path('tijian_list/',views.tijian_list),
    path('user_list/',views.user_list),
    path('add_user/',views.add_user),
path('delete_user/',views.delete_user),
    path('edit_user/',views.edit_user),
    path('department_list/',views.department_list),
    path('add_department/',views.add_department),
    path('edit_department/',views.edit_department),
    path('delete_department/',views.delete_department),
    path('doctor_list/',views.doctor_list),
    path('add_doctor/',views.add_doctor),
    path('edit_doctor/',views.edit_doctor),
    path('delete_doctor/',views.delete_doctor),
    path('edit_tijian/',views.edit_tijian),
    path('delete_tijian/',views.delete_tijian),
    path('medicine_list/',views.medicine_list),
path('edit_medicine/',views.edit_medicine),
    path('delete_medicine/', views.delete_medicine),
    path('order_list/',views.order_list),
path('edit_order/',views.edit_order),
path('add_order/',views.add_order),
    path('goods_list/',views.goods_list),
    path('search_doctor/',views.search_doctor, name='search_doctor'),
    path('search_user/',views.search_user, name='search_user'),
    path('search_medicine/',views.search_medicine, name='search_medicine'),
    path('add_medicine/', views.add_medicine),
    path('tj_order_list/',views.TjOrder_list),
    path('add_TjOrder/',views.add_TjOrder),
path('edit_tijian_order/',views.edit_tijian_order),
path('article_list/',views.Article_list),
    path('add_article/', views.add_article),
    path('edit_article/',views.edit_article),
    path('search_article/',views.search_article,name='search_article'),
path('tj_order_list_0/',views.TjOrder_list_0),
path('pass_tijian_0/', views.pass_tijian_0, name='pass_tijian_0'),
path('order_list_0/',views.order_list_0),
path('pass_order_0/', views.pass_order_0, name='pass_order_0'),
    path('guanli_index/',views.guanli_index),
    path('test/', views.test),



    ]